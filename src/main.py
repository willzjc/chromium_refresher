import urllib.request
import os ,sys, logging, inspect, traceback, shutil, zipfile

config = {
    k:v for k,v in [line.split('=',maxsplit=1)
        for line in open('../ref/config.ini','r').read().split('\n')
            if len(line.strip())>0]
         }

formatter = logging.Formatter( '%(asctime)s [%(levelname)s] [%(filename)s|%(lineno)s - %(funcName)s()]: %(message)s',
                               datefmt= '%Y-%m-%d %I:%M:%S %p')
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(fmt=formatter)
logger.addHandler(hdlr=handler)
logger.setLevel('DEBUG')
logger.propagate = False  # prevents double printing

TARGET_FILE_NAME="chrome.zip"

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

def download_ops(current_version):
    '''once download is required - trigger this function'''
    # File downloading operations
    local_pathway = '../target/versions/%s' % current_version
    local_pathway = check_path(os.path.realpath(local_pathway))
    chrome_file = TARGET_FILE_NAME
    pathway_new_version_of_chrome = local_pathway + '/' + chrome_file
    logger.info('Starting urllib.request.urlretrieve to %s' % pathway_new_version_of_chrome)
    urllib.request.urlretrieve(url, pathway_new_version_of_chrome)
    return pathway_new_version_of_chrome

def disk_ops(pathway_new_version_of_chrome,target_extraction_folder=None, archive_folder=None):
    '''remove current version, replace with existing version'''
    interim_chromium_zip_folder=os.path.abspath('../target/current/')
    logger.info("Copying from %s to %s"%(pathway_new_version_of_chrome,interim_chromium_zip_folder))
    shutil.copy(src=pathway_new_version_of_chrome, dst=check_path(interim_chromium_zip_folder))

    logger.info("Now Extract all contents to %s"%target_extraction_folder)
    target_extraction_folder=interim_chromium_zip_folder if target_extraction_folder is None else target_extraction_folder
    with zipfile.ZipFile('%s/%s'%(interim_chromium_zip_folder,TARGET_FILE_NAME), 'r') as zipObj:
        # Extract all the contents of zip file in current directory
        zipObj.extractall(target_extraction_folder)

    version=pathway_new_version_of_chrome.replace('\\','/').split('/')[-2]

    logger.info("Finished extraction")
    if not archive_folder is None:
        logger.info("Archiving this version to %s"%archive_folder)
        src,dst=target_extraction_folder,archive_folder+'/'+version
        logger.info("sh.copy from %s to %s"%(src,dst))
        shutil.copytree(src=src,dst=dst)

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
        pathway_new_version_of_chrome=download_ops(current_version)

        logger.info("File downloaded to %s, now copying to current path" % pathway_new_version_of_chrome)
        disk_ops(
            pathway_new_version_of_chrome,
            'c:/local/app/chromium/current',
            'c:/local/app/chromium'
        )