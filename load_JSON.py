import json


def load_JSONFile(file):
    # 打开 JSON 文件
    with open(file, 'r') as json_file:
        # 读取文件内容并解析为字典
        data_dict = json.load(json_file)

    # {"searchList":[],"dirList":["css\/\/","img\/\/","js\/\/","movie\/\/","public\/\/"]}
    #['file', 'hima920230524100000fd.png', 145158337, '2023/05/24 10:23:55', '/osn-disk/webuser/wsdb/share_directory/bDw2maKV/png/Pifd/2023/05-24/10']    
    arr=[]
    result=[]
    for data in ((data_dict)):
        dic=((json.loads(data)))
        if not dic['searchList']:
            continue
        d=(dic['searchList'])
        arr.extend(d)


    for i in range(len(arr)):
        a=arr[i]
        hashUrl=a[-1].split('/')[5]
        d_url=a[-1]+'/'+a[1]
        dic={'name':a[1],
            'hashUrl':hashUrl,
            'd_url':d_url
        }
        result.append(dic)
    return(result)



def load_JSON(json_str):

    data_dict = json.loads(json_str)
    
    if not data_dict['searchList']:
        return 
    searchList=(data_dict['searchList'])
    


    for i in range(len(searchList)):
        a=searchList[i]
        hashUrl=a[-1].split('/')[5]
        d_url=a[-1]+'/'+a[1]
        dic={'name':a[1],
            'hashUrl':hashUrl,
            'd_url':d_url
        }
        yield (dic)
if __name__ == "__main__":
#{'name': 'hima920230524100000fd.png', 'hashUrl': 'bDw2maKV', 'd_url': '/osn-disk/webuser/wsdb/share_directory/bDw2maKV/png/Pifd/2023/05-24/10/hima920230524100000fd.png'}
    aa='''['{"searchList":[["file","hima920240101010000fd.png",8891045,"2024\\/01\\/01 01:27:42","\\/osn-disk\\/webuser\\/wsdb\\/share_directory\\/bDw2maKV\\/png\\/Pifd\\/2024\\/01-01\\/01"],["file","hima920240101011000fd.png",9947368,"2024\\/01\\/01 01:32:42","\\/osn-disk\\/webuser\\/wsdb\\/share_directory\\/bDw2maKV\\/png\\/Pifd\\/2024\\/01-01\\/01"],["file","hima920240101012000fd.png",11103289,"2024\\/01\\/01 01:42:42","\\/osn-disk\\/webuser\\/wsdb\\/share_directory\\/bDw2maKV\\/png\\/Pifd\\/2024\\/01-01\\/01"],["file","hima920240101013000fd.png",12360541,"2024\\/01\\/01 01:52:43","\\/osn-disk\\/webuser\\/wsdb\\/share_directory\\/bDw2maKV\\/png\\/Pifd\\/2024\\/01-01\\/01"],["file","hima920240101014000fd.png",13714219,"2024\\/01\\/01 03:02:42","\\/osn-disk\\/webuser\\/wsdb\\/share_directory\\/bDw2maKV\\/png\\/Pifd\\/2024\\/01-01\\/01"],["file","hima920240101015000fd.png",15213734,"2024\\/01\\/01 03:02:44","\\/osn-disk\\/webuser\\/wsdb\\/share_directory\\/bDw2maKV\\/png\\/Pifd\\/2024\\/01-01\\/01"]],"dirList":null}']'''
    # c='{"searchList":[["file","hima920240101010000fd.png",8891045,"2024\/01\/01 01:27:42","\/osn-disk\/webuser\/wsdb\/share_directory\/bDw2maKV\/png\/Pifd\/2024\/01-01\/01"],["file","hima920240101011000fd.png",9947368,"2024\/01\/01 01:32:42","\/osn-disk\/webuser\/wsdb\/share_directory\/bDw2maKV\/png\/Pifd\/2024\/01-01\/01"],["file","hima920240101012000fd.png",11103289,"2024\/01\/01 01:42:42","\/osn-disk\/webuser\/wsdb\/share_directory\/bDw2maKV\/png\/Pifd\/2024\/01-01\/01"],["file","hima920240101013000fd.png",12360541,"2024\/01\/01 01:52:43","\/osn-disk\/webuser\/wsdb\/share_directory\/bDw2maKV\/png\/Pifd\/2024\/01-01\/01"],["file","hima920240101014000fd.png",13714219,"2024\/01\/01 03:02:42","\/osn-disk\/webuser\/wsdb\/share_directory\/bDw2maKV\/png\/Pifd\/2024\/01-01\/01"],["file","hima920240101015000fd.png",15213734,"2024\/01\/01 03:02:44","\/osn-disk\/webuser\/wsdb\/share_directory\/bDw2maKV\/png\/Pifd\/2024\/01-01\/01"]],"dirList":null}'
    cc='{"searchList":[],"dirList":null}'
    for i in (load_JSON(cc)):

        print(i)
