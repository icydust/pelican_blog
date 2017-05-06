pkill -9 python
cd /media/cai/work/Coding/blog/test
pelican content/posts
cd /media/cai/work/Coding/blog/test/output
python -m pelican.server
