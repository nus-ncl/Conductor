import sys
import wget

def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)
def main():

    url = 'https://github.com/hkwany/VIndex/blob/dev/VIndex/log4shell/deploy/deploy.zip'
    wget.download(url)
    # download_url("https://github.com/hkwany/VIndex/blob/dev/VIndex/log4shell/deploy/deploy.zip", "deploy.zip")
    # urllib.request.urlretrieve("https://github.com/hkwany/VIndex/tree/dev/VIndex/log4shell/deploy/deploy.zip", "deploy.zip")
    # if (len(sys.argv) == 2) and (sys.argv[1] == "test"):
    #     test()
    #     print
    #     "Pass all test"
    #     exit()
    # elif (len(sys.argv) == 4) and (sys.argv[1] == "project") and (sys.argv[2] == "netdef-input"):
    #     with open(sys.argv[3], 'r') as afile:
    #         file_content = afile.read()
    #
    #     netdef = json.loads(file_content)
    #     import vagrantfile
    #     vagrantfile.produce_nsfile(netdef)
    #     vagrantfile.produce_vf(netdef)
    #     vagrantfile.produce_ansible(netdef)
    #     vagrantfile.produce_hostfile(netdef)
    #     vagrantfile.produce_runcmd(netdef)
    # elif (len(sys.argv) == 4) and (sys.argv[1] == "ns") and (sys.argv[2] == "netdef-input"):
    #     with open(sys.argv[3], 'r') as afile:
    #         file_content = afile.read()
    #
    #     netdef = json.loads(file_content)
    #     import vagrantfile
    #     vagrantfile.produce_nsfile(netdef)
    # elif (len(sys.argv) == 3) and (sys.argv[1] == "project"):

if __name__ == '__main__':
    main()
    a=1
    if (a==1):
        a
    else:
        b