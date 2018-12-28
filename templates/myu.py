import json

def main():
    f = open("myu_s.json", 'r')

    #ココ重要！！
    json_data = json.load(f) #JSON形式で読み込む

    name_list = ["honoka","eri","kotori","umi","rin","maki","nozomi","hanayo","niko"]
    for name in name_list:  #上のネームリストがなくなるまでループ
        print("{0:6s} 身長：{1}cm BWH: ".format(name,json_data[name]["height"]),end="\t")
        # {0:6s}=0番目の配列、6文字で幅をそろえる
        for i in range(len(json_data[name]["BWH"])):
            print("{}".format(json_data[name]["BWH"][i]),end="\t")
        print()


if __name__=='__main__':
    main()