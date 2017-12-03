pkill -9 python
cd /media/cai/work/Coding/newBlog
pelican content
cd /media/cai/work/Coding/newBlog/output
python -m pelican.server
