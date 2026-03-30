const { chromium } = require('playwright');

const urls = [
  { headline: '[AI혁명](189)"AI 수익비중 50%가 목표"....기업의 AX 파트너 베스핀글로벌', url: 'https://view.asiae.co.kr/article/2026030515494076374', source: '아시아경제' },
  { headline: '오픈AI 연환산매출 37조원…앤스로픽 추격, MS 변수에 경쟁 격화', url: 'https://n.news.naver.com/mnews/article/018/0006229977', source: '이데일리' },
  { headline: '오픈AI·오라클, 텍사스주 스타게이트 데이터센터 확장 백지화', url: 'https://n.news.naver.com/mnews/article/001/0015943473', source: '연합뉴스' },
  { headline: 'AI 코딩도구 코덱스 국내서 인기…주간이용자 급증', url: 'https://n.news.naver.com/mnews/article/001/0015944373', source: '연합뉴스' },
  { headline: 'AI도 앱스토어 시대…앤스로픽, 클로드 마켓플레이스 공개', url: 'https://n.news.naver.com/mnews/article/018/0006230256', source: '이데일리' },
];

(async () => {
  const browser = await chromium.launch({ headless: true });
  const results = [];

  for (const item of urls) {
    try {
      const page = await browser.newPage();
      await page.goto(item.url, { waitUntil: 'domcontentloaded', timeout: 15000 });
      const title = await page.title();
      let text = '';
      try {
        text = await page.locator('article, #dic_area, .newsct_article, .article_body, main').first().innerText({ timeout: 5000 });
      } catch {
        text = await page.locator('body').innerText({ timeout: 5000 });
      }
      const summary = text.replace(/\s+/g, ' ').trim().substring(0, 300);
      results.push({ ...item, title, summary });
      await page.close();
    } catch (e) {
      results.push({ ...item, title: item.headline, summary: '[접속 불가: ' + e.message.substring(0, 50) + ']' });
    }
  }

  await browser.close();
  console.log(JSON.stringify(results, null, 2));
})();
