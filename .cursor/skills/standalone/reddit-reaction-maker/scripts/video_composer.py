"""Video composer — assembles background, card overlays, TTS audio, and BGM."""

import os
import re
from pathlib import Path

from moviepy import (
    AudioFileClip,
    ColorClip,
    CompositeAudioClip,
    CompositeVideoClip,
    ImageClip,
    VideoFileClip,
)
from rich.console import Console

from .background_downloader import (
    random_start_time,
    select_random_audio,
    select_random_video,
    setup_backgrounds,
)

console = Console()


def _sanitize_filename(text: str) -> str:
    safe = re.sub(r'[<>:"/\\|?*]', "", text)
    safe = re.sub(r"\s+", "_", safe)
    return safe[:80]


class VideoComposer:
    def __init__(self, config: dict):
        self.width = config.get("video_width", 1080)
        self.height = config.get("video_height", 1920)
        self.fps = config.get("fps", 30)
        self.max_duration = config.get("max_duration_seconds", 58)
        self.background_dir = config.get("background_dir", "assets/backgrounds")
        self.opacity = config.get("bg_opacity", 0.7)
        self.screenshot_scale = config.get("screenshot_scale", 0.90)
        self.bgm_enabled = config.get("bgm_enabled", True)
        self.bgm_volume = config.get("bgm_volume", 0.15)

        setup_backgrounds(self.background_dir)

    def _create_background(self, duration: float) -> CompositeVideoClip | ColorClip:
        bg_path = select_random_video(self.background_dir)

        if bg_path is None:
            console.print("[yellow]No background video. Using solid color.[/yellow]")
            return ColorClip(size=(self.width, self.height), color=(20, 20, 30), duration=duration)

        console.print(f"  [dim]Background: {os.path.basename(bg_path)}[/dim]")
        video = VideoFileClip(bg_path)

        start = random_start_time(video.duration, duration)
        video = video.subclipped(start, start + min(duration, video.duration - start))

        vid_w, vid_h = video.size
        target_ratio = self.width / self.height

        if vid_w / vid_h > target_ratio:
            new_w = int(vid_h * target_ratio)
            x_off = (vid_w - new_w) // 2
            video = video.cropped(x1=x_off, x2=x_off + new_w)
        else:
            new_h = int(vid_w / target_ratio)
            y_off = (vid_h - new_h) // 2
            video = video.cropped(y1=y_off, y2=y_off + new_h)

        video = video.resized((self.width, self.height))

        dim = ColorClip(
            size=(self.width, self.height), color=(0, 0, 0), duration=duration
        ).with_opacity(1 - self.opacity)

        return CompositeVideoClip([video, dim])

    def _create_card_clip(self, card_path: str, duration: float) -> ImageClip | None:
        if not card_path or not os.path.exists(card_path):
            return None

        try:
            clip = ImageClip(card_path, duration=duration)

            img_w, img_h = clip.size
            target_w = int(self.width * self.screenshot_scale)
            if img_w > target_w:
                clip = clip.resized(target_w / img_w)

            img_w, img_h = clip.size
            max_h = int(self.height * 0.75)
            if img_h > max_h:
                clip = clip.resized(max_h / img_h)

            img_w, img_h = clip.size
            x = (self.width - img_w) // 2
            y = (self.height - img_h) // 2
            return clip.with_position((x, y))
        except Exception as e:
            console.print(f"  [yellow]Card clip error: {e}[/yellow]")
            return None

    def _create_bgm(self, duration: float) -> AudioFileClip | None:
        if not self.bgm_enabled:
            return None

        path = select_random_audio(self.background_dir)
        if not path:
            return None

        console.print(f"  [dim]BGM: {os.path.basename(path)} (vol: {self.bgm_volume})[/dim]")
        try:
            bgm = AudioFileClip(path)
            if bgm.duration >= duration:
                bgm = bgm.subclipped(0, duration)
            return bgm.with_volume_scaled(self.bgm_volume)
        except Exception as e:
            console.print(f"  [yellow]BGM error: {e}[/yellow]")
            return None

    def compose(
        self,
        post_id: str,
        post_title: str,
        segments: list[dict],
        output_dir: str,
    ) -> str | None:
        if not segments:
            console.print("[red]No segments to compose.[/red]")
            return None

        console.print(f"[cyan]Composing video for: {post_title[:50]}...[/cyan]")

        try:
            audio_clips = []
            timing: list[tuple[float, float, dict]] = []
            t = 0.0
            gap = 0.5

            for seg in segments:
                audio = AudioFileClip(seg["audio_path"])
                dur = audio.duration

                if t + dur > self.max_duration:
                    audio.close()
                    break

                audio_clips.append(audio.with_start(t))
                timing.append((t, dur, seg))
                t += dur + gap

            if not audio_clips:
                console.print("[red]No audio within duration limit.[/red]")
                return None

            total = min(t - gap, self.max_duration)

            bg = self._create_background(total)

            overlays = []
            for start, dur, seg in timing:
                clip = self._create_card_clip(seg.get("card_path", ""), dur)
                if clip:
                    overlays.append(clip.with_start(start))

            final = CompositeVideoClip([bg] + overlays, size=(self.width, self.height))

            tts_audio = CompositeAudioClip(audio_clips)
            bgm = self._create_bgm(total)
            mixed = CompositeAudioClip([tts_audio, bgm.with_start(0)]) if bgm else tts_audio

            final = final.with_audio(mixed).with_duration(total)

            os.makedirs(output_dir, exist_ok=True)
            filename = _sanitize_filename(f"reddit_{post_id}_{post_title[:30]}")
            output_path = os.path.join(output_dir, f"{filename}.mp4")

            console.print(f"  [dim]Rendering {total:.1f}s video...[/dim]")
            final.write_videofile(
                output_path,
                fps=self.fps,
                codec="libx264",
                audio_codec="aac",
                bitrate="8M",
                preset="medium",
                logger=None,
            )

            final.close()
            for ac in audio_clips:
                ac.close()
            if bgm:
                bgm.close()

            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            console.print(
                f"  [green]✓[/green] Saved: {output_path} ({total:.1f}s, {size_mb:.1f}MB)"
            )
            return output_path

        except Exception as e:
            console.print(f"[red]Composition error: {e}[/red]")
            import traceback
            traceback.print_exc()
            return None
