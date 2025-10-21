#PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-09-Sprint4" --force
#PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-10-Sprint4" --force


#PYTHONPATH=. python scripts/sprint_stats.py --sprint "25-10-Sprint4" --notion-parent-id "2939eddc34e680f58c7ad076e5ba3e88"


# Dry run 테스트
#PYTHONPATH=. python scripts/create_new_database_sync.py --parent-page-id 2939eddc34e68064b505c66d3c22b27a --database-title "GitHub Sync Test" --dry-run

# 실제 실행
#PYTHONPATH=. python scripts/create_new_database_sync.py --parent-page-id 2939eddc34e68064b505c66d3c22b27a --database-title "GitHub Project Sync" --sprint-filter "25-10-Sprint4"

PYTHONPATH=. python scripts/create_new_database_sync.py \
  --parent-page-id 2939eddc34e68064b505c66d3c22b27a \
  --sprint-filter "25-10-Sprint4"