import urllib.request
import os ,sys, logging, inspect, traceback, shutil

config = {
    k:v for k,v in [line.split('=',maxsplit=1)
        for line in open('../ref/config.ini','r').read().split('\n')
            if len(line.strip())>0]
         }

# fmt =
# datefmt =

formatter = logging.Formatter( '%(asctime)s [%(levelname)s] [%(filename)s|%(lineno)s - %(funcName)s()]: %(message)s',
                               datefmt= '%Y-%m-%d %I:%M:%S %p')
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(fmt=formatter)
logger.addHandler(hdlr=handler)
logger.setLevel('DEBUG')
logger.propagate = False  # prevents double printing


def check_path(path):
    """Checks if path exists, create folder iteratively if not"""
    path=path.replace('\\','/')
    if not os.path.exists(path):
        each_folder_element=path.split('/')
        for i in range(0,len(each_folder_element)):
            pathway='/'.join(each_folder_element[0:i+1])
            if not os.path.exists(pathway):
                print('pathway %s does not exist, creating...'%pathway)
                os.mkdir(pathway)
    return path

if __name__=='__main__':
    logger.info(config)
    url = config['URL']
    last_change_url=config['LASTCHANGE_URL']

    version_ref='../ref/current_version.txt'

    if not os.path.exists(version_ref):
        f=open(version_ref,'w')
        f.write('')
        f.close()

    prev_version=open(version_ref,'r').read().strip()
    urllib.request.urlretrieve(last_change_url, version_ref)
    current_version=open(version_ref,'r').read().strip()

    if prev_version != current_version:
        logger.info('Prev Version is no longer equal to current version\n%s vs %s'%(prev_version,current_version))

        # File downloading operations
        local_pathway='../target/versions/%s'%current_version
        local_pathway=check_path(os.path.realpath(local_pathway))
        chrome_file='chromium.zip'
        new_version_of_chrome= local_pathway + '/' + chrome_file
        logger.info('Starting urllib.request.urlretrieve to %s' % new_version_of_chrome)
        urllib.request.urlretrieve(url, new_version_of_chrome)
        logger.info("File downloaded to %s, now copying to current path" % new_version_of_chrome)
        shutil.copy(src=new_version_of_chrome,dst=check_path('../target/current/'))