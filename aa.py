# HIから入力
# 過去に入力されたアプリの要件と被っていないか比較
# 結果を反映してデータベースへ保存
#
# C-CONTから経路情報を受け取る
# 現在時刻でiot_tableを検索して優先させるアプリはないか
#   現在時刻がstartのアプリを検索
#   該当するWAPにそのアプリを利用するデバイスが存在
#   他のアプリを利用しているが、同じgwを利用しているWAPがある
#   関係ないアプリのWAPを他のGWへ接続するためのルール
#
#
# あったらそのデバイスを優先させる処理
# Operationへ送信

# C-CONTから受け取る情報
# 実際につながっているルート     rote(gw1-wap1,gw2-wap2)
# 通信可能なルート              unused-rote(gw1-wap2,gw2-wap3)
# デバイスが使用しているアプリ名 or IPアドレス     use-app(d1-aa,d2-aa,d3-bb)
#
data = {"rote":('gw1-wap1-d1','gw2-wap2-d2','gw2-wap3-d3'), "unused-rote":("gw1-wap2",""),"use-app":("d1-aa","d2-aa","d3-bb") }
print(data)
# print(data["rote"])
# print(data["unused-rote"])
# print(data["use-app"])

i = 0
aa = {}
name = "bb"     #優先度の高いアプリ名
# 優先度が高いアプリを使用しているアプリがあるか
for n in data["use-app"]:
    aa[i] = n
    test = aa[i].find(name)
    if test > 1:
        print(aa[i])
        device = aa[i][0:2]
        print(device)
    i += 1

# 優先度が高いアプリを使用しているデバイスがあった
