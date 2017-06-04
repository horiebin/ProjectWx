import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from dao.auto_reply import AutoReplyDao

if __name__ == "__main__":
    AutoReplyDao().saveReplysToMc()