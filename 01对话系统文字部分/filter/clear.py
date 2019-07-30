# coding:utf-8

import xlrd

def readFile():
    data = xlrd.open_workbook("./123.xlsx")
    table = data.sheet_by_index(0)
    # print(table.row_values(0))
    numRows = table.nrows
    print("numRows",numRows)

    sentences = []
    for i in range(numRows):
        sentences.append(table.row_values(i)[0])
    # print(sentences)
    return sentences

def process(sentences):
    numSent = len(sentences)
    print(numSent)
    for i in range(numSent):
        # print("sentences[i]",i,"  ",sentences[i])
        sentences[i] = str(sentences[i])
        if len(sentences[i])>20:
            sentences[i] = sentences[i][:20]
        sentences[i] = sentences[i].replace(" ","")
        sentences[i] = sentences[i].replace("-","")
    return sentences

def saveFile(sentences):
    f = open("./data.txt",'w')
    for sentence in sentences:
        f.write(sentence+'\n')

    f.close()


def main():
    sentences = readFile()
    sentences = process(sentences)
    saveFile(sentences)

main()