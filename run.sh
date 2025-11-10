#PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-09-Sprint4" --force
#PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-10-Sprint4" --force

#PYTHONPATH=. python scripts/create_new_database_sync.py \
#  --parent-page-id 2939eddc34e68064b505c66d3c22b27a \
#  --sprint-filter "25-10-Sprint4"

# 기본 사용
#PYTHONPATH=. python scripts/copy_database_and_sync.py \
#  --parent-page-id 2939eddc34e68064b505c66d3c22b27a \
#  --database-title "내 새로운 데이터베이스"

# Sprint 필터링
#PYTHONPATH=. python scripts/copy_database_and_sync.py \
#  --parent-page-id 2939eddc34e68064b505c66d3c22b27a \
#  --sprint-filter "25-10-Sprint4"

# Dry-run 모드 (미리보기)
#PYTHONPATH=. python scripts/copy_database_and_sync.py \
#  --parent-page-id 2939eddc34e68064b505c66d3c22b27a \
#  --dry-run


PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-10-Sprint4" --force

PYTHONPATH=. python scripts/sprint_pr_review_check.py --sprint "25-10-Sprint4" --notion-parent-id "2939eddc34e680f58c7ad076e5ba3e88"

PYTHONPATH=. python scripts/sprint_stats.py --sprint "25-10-Sprint4" --notion-parent-id "2939eddc34e680f58c7ad076e5ba3e88"
