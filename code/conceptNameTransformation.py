import itertools
import spacy
from spacy.tokenizer import Tokenizer #split by space #default for Tokenizer
nlp = spacy.load("en_core_web_lg")
nlp.tokenizer = Tokenizer(nlp.vocab)
#
#example = "basal cell carcinoma of left cell eyelid".lower()
#example = "basal cell neoplasm".lower()
#
alterDictonary = {}
def upperGenerator(conceptName1):
    doc = nlp(conceptName1)
    tokenList = [token for token in doc]
    nounChunksList = [nounChunks for nounChunks in doc.noun_chunks]
    readyForComb = []
    paralel = 0 
    PureSecondaryOrNot = 0
    chunkedListForParalel = []
    if nounChunksList!=[]:
        chunkedList = decomposite(tokenList,nounChunksList)
        chunkedListCopy = chunkedList[:]
        for item666 in chunkedListCopy:
            if type(item666) == list:
                chunkedListForParalel.append([" ".join(tokenDic.get(x666.text) for x666 in item666[0])])
            else:
                chunkedListForParalel.append([tokenDic.get(item666.text)])
        if len(chunkedList) > 1:  #otherwise whole concept name as a noun phrase
            for k in range(0,len(chunkedList)):
                if type(chunkedList[k]) == list:
                    nounPhraseStr = " ".join(tokenDic.get(x.text) for x in chunkedList[k][0])
                    if nameStrToAUI.get(nounPhraseStr,"Default") != "Default":
                        if alterDictonary.get(nounPhraseStr,"Default") != "Default":
                            readyForComb.append(alterDictonary.get(nounPhraseStr))
                        else:
                            AUI1s = nameStrToAUI.get(nounPhraseStr)
                            alterStr = []
                            alterStr.append(nounPhraseStr) #did not add this CUI's synonyms
                            for AUI1 in AUI1s:
                                if AUI1 in allNodesInUMLSSet:
                                    AUI1Ancestor = findKLevelAncestors(AUI1)
                                    for ancestor in AUI1Ancestor:
                                        if AUItoNameStr.get(ancestor,"Default") != "Default":
                                            ancestorStr = AUItoNameStr.get(ancestor)
                                            alterStr.extend(ancestorStr)
                            secondaryComb = []
                            secondaryNounPhrase = secondaryNP(chunkedList[k])
                            if secondaryNounPhrase != "NO Clean SubNP":
                                secondaryChunkedList = decomposite(chunkedList[k][0],[secondaryNounPhrase])
                                for j in range(0,len(secondaryChunkedList)):
                                    if type(secondaryChunkedList[j]) == list:
                                        nounPhraseStr2 = " ".join(tokenDic.get(x.text) for x in secondaryChunkedList[j][0])
                                        if nameStrToAUI.get(nounPhraseStr2,"Default") != "Default":
                                            if alterDictonary.get(nounPhraseStr2,"Default") != "Default":
                                                secondaryComb.append(alterDictonary.get(nounPhraseStr2))
                                            else:
                                                AUI1s = nameStrToAUI.get(nounPhraseStr2)
                                                alterStr2 = []
                                                alterStr2.append(nounPhraseStr2) #did not add this CUI's synonyms
                                                for AUI1 in AUI1s:
                                                    if AUI1 in allNodesInUMLSSet:
                                                        AUI1Ancestor = findKLevelAncestors(AUI1)
                                                        for ancestor in AUI1Ancestor:
                                                            if AUItoNameStr.get(ancestor,"Default") != "Default":
                                                                ancestorStr = AUItoNameStr.get(ancestor)
                                                                alterStr2.extend(ancestorStr)
                                                secondaryComb.append(alterStr2)
                                                alterDictonary[nounPhraseStr2] = list(set(alterStr2)) 
                                        else:
                                            secondaryComb.append([nounPhraseStr2])            
                                    else:
                                        secondaryComb.append([tokenDic.get(secondaryChunkedList[j].text)])
                            if secondaryComb!=[]:
                                secondaryCombinations = list(itertools.product(*secondaryComb))
                                secondaryAlterStr = [" ".join(list(y)) for y in secondaryCombinations ]
                                alterStr.extend(secondaryAlterStr)
                            newAlterStr = list(set(alterStr))
                            readyForComb.append(newAlterStr)
                            if len(newAlterStr)!=1:
                                paralel = paralel+1
                            alterDictonary[nounPhraseStr] = newAlterStr
                    else:
                        readyForComb.append([nounPhraseStr])
                else:
                    readyForComb.append([tokenDic.get(chunkedList[k].text)])
        else:
            PureSecondaryOrNot = 1
            secondaryNounPhrase = secondaryNP(chunkedList[0]) #inputList: [[],root]
            if secondaryNounPhrase != "NO Clean SubNP":
                secondaryChunkedList = decomposite(chunkedList[0][0],[secondaryNounPhrase])
                for k in range(0,len(secondaryChunkedList)):
                    if type(secondaryChunkedList[k]) == list:
                        nounPhraseStr = " ".join(tokenDic.get(x.text) for x in secondaryChunkedList[k][0])
                        if nameStrToAUI.get(nounPhraseStr,"Default") != "Default":
                            if alterDictonary.get(nounPhraseStr,"Default") != "Default":
                                readyForComb.append(alterDictonary.get(nounPhraseStr))
                            else:
                                AUI1s = nameStrToAUI.get(nounPhraseStr)
                                alterStr = []
                                alterStr.append(nounPhraseStr) #did not add this CUI's synonyms
                                for AUI1 in AUI1s:
                                    if AUI1 in allNodesInUMLSSet:
                                        AUI1Ancestor = findKLevelAncestors(AUI1)
                                        for ancestor in AUI1Ancestor:
                                            if AUItoNameStr.get(ancestor,"Default") != "Default":
                                                ancestorStr = AUItoNameStr.get(ancestor)
                                                alterStr.extend(ancestorStr)
                                newAlterStr = list(set(alterStr))
                                alterDictonary[nounPhraseStr] = newAlterStr
                                readyForComb.append(newAlterStr)
                        else:
                            readyForComb.append([nounPhraseStr])            
                    else:
                        readyForComb.append([tokenDic.get(secondaryChunkedList[k].text)])
        varAmount = 1
        if PureSecondaryOrNot == 1:
            paralel = "PureSecondary"
        for varItem in readyForComb:
            varAmount = varAmount * len(varItem)
        if varAmount <100000000: # #memory limitation
            combinations = list(itertools.product(*readyForComb))
            return (combinations,chunkedList,paralel,chunkedListForParalel)   
        else:
            return ([],[],paralel,chunkedListForParalel)
    #if any combination is returned, won't come to this line of code 
    return([],[],paralel,chunkedListForParalel)       
#
def decomposite(inputTokenList,inputNounChunksList):
    chunkedList1 = []
    combinedTokenForChunk = []
    index1 = 0 #nounChunkToBeLocate
    for i in range(0,len(inputTokenList)):
        if index1 < len(inputNounChunksList):
            if inputTokenList[i] in inputNounChunksList[index1]:
                combinedTokenForChunk.append(inputTokenList[i])
            else:
                #deal with things before inputTokenList[i] (if exists)
                if len(combinedTokenForChunk)>0:
                    #print("1")
                    if type(inputNounChunksList[index1]) != list:   #store root information
                    #decomposite based on base noun phrase (inputNounChunksList:[np1,np2,np3])
                        chunkedList1.append([combinedTokenForChunk,inputNounChunksList[index1].root])
                    else:
                    #decomposite based on secondary noun phrase (inputNounChunksList: [[T1,T2,T3]] )
                        chunkedList1.append([combinedTokenForChunk])
                    combinedTokenForChunk = []
                    index1 = index1+1
                #deal with inputTokenList[i]
                if index1 <len(inputNounChunksList):
                    if inputTokenList[i] not in inputNounChunksList[index1]:
                        chunkedList1.append(inputTokenList[i])
                    else:
                        combinedTokenForChunk.append(inputTokenList[i])
                else:
                    chunkedList1.append(inputTokenList[i])
        else:
            chunkedList1.append(inputTokenList[i])
    if len(combinedTokenForChunk)>0:
        if type(inputNounChunksList[index1]) != list:
            chunkedList1.append([combinedTokenForChunk,inputNounChunksList[index1].root])
        else:
            chunkedList1.append([combinedTokenForChunk])
        combinedTokenForChunk = []
    return chunkedList1
#      
def secondaryNP(inputList): # inputList: [[list of token], root]  #output: [token,token,token]
    count = 0
    secondaryRoot = []
    for singleWord in inputList[0]:
        if singleWord != inputList[1]:
            if singleWord.head == inputList[1] and singleWord.pos_ == "NOUN":
                count = count +1
                secondaryRoot.append(singleWord)
    if count == 1:   
    #if more than 2 noun are there to modify the root of the noun chunk, 
    #it usually indicate the base noun phrase is not identified properly
        secondaryPhrase = [secondaryRoot[0]]
        current = [secondaryRoot[0]]
        while current!=[]:
            currentNode = current.pop()
            aaa = list(currentNode.children)
            if len(aaa)>1:
                return "NO Clean SubNP"
            elif len(aaa) == 1:
                if aaa[0].nbor() == currentNode:   # nbor return token on [i+1] position for token on [i]
                    current.append(aaa[0])
                    secondaryPhrase.insert(0,aaa[0])
        if len(secondaryPhrase)>1: # it could be >= 1
            return secondaryPhrase
        else:
            return "NO Clean SubNP"
    else:
        return "NO Clean SubNP"
#    
###############################################################################    
import networkx as nx
file2 = open("hierarchicalRelation(childParent)2019AB_AUIISA.txt","rb") 
#The content for each row: child\tparent\n
Dirgraph1 = nx.read_edgelist(file2, create_using = nx.DiGraph(), nodetype = str)
allNodesInUMLS = sorted(list(Dirgraph1.nodes)) 
allNodesInUMLSSet = set(allNodesInUMLS)
allSubRoot = [n for n,d in Dirgraph1.out_degree() if d==0] 
file2.close()
#
def findAncestors(node):
    Dic = dict(nx.bfs_successors(Dirgraph1,node))
    d = Dic.values()
    c = []
    for e in d:
        c = c+e
    return c  
#
#Limitation of Ancestor.
def findKLevelAncestors(node):
    Dic = dict(nx.bfs_successors(Dirgraph1,node,depth_limit=2))   
    #Dic = dict(nx.bfs_successors(Dirgraph1,node))   
    d = Dic.values()
    c = []
    for e in d:
        c = c+e
    return c  
#
###############################################################################
nameStrToAUI = {} #str should be lower case
AUItoNameStr = {}
AUItoCUI = {}
import csv
file1 = open("conceptName2019AB_FromNormalizedToken.csv","r")
#The content for each row: normalized concept name, CUI, source, ID in source, Pre or not, AUI, original concept name
reader1 = csv.reader(file1)
for row1 in reader1:
    name1 = row1[0].lower()
    if nameStrToAUI.get(name1,"Default") == "Default":
        nameStrToAUI[name1] = [row1[5]]
    else:
        if row1[5] not in nameStrToAUI.get(name1):
            nameStrToAUI[name1].append(row1[5])
    if AUItoNameStr.get(row1[5],"Default") == "Default":
        AUItoNameStr[row1[5]] = [name1]
    else:
        if name1 not in AUItoNameStr.get(row1[5]):
            print("error!")  #validate that one AUI only map to one string
            AUItoNameStr[row1[5]].append(name1)
    if AUItoCUI.get(row1[5],"Default") == "Default":
        AUItoCUI[row1[5]] = [row1[1]]
    else:
        if row1[1] not in AUItoCUI.get(row1[5]):
            print("error!")
            AUItoCUI[row1[5]].append(row1[1])
file1.close()
#
tokenDic = {}
file1new = open("tokenDictionary.csv","r")
#The content for each row: token, normalized token
#
reader1new = csv.reader(file1new)
for row1new in reader1new:
    tokenDic[row1new[0]] = row1new[1]
file1new.close()
#
nameStringToAUI_Original = {}
file1 = open("conceptName2019AB.csv","r")
#The content for each row: concept name, CUI, source, ID in source, Pre or not, AUI
reader1 = csv.reader(file1)
for row1 in reader1:
    name1 = row1[0].lower()
    #count.add(name1)
    if nameStringToAUI_Original.get(name1,"Default") == "Default":
        nameStringToAUI_Original[name1] = [row1[5]]
    else:
        if row1[5] not in nameStringToAUI_Original.get(name1):
            nameStringToAUI_Original[name1].append(row1[5])
file1.close()
###############################################################################
#E.g, Cell Function, Disease or Syndrome
semanticType = {}
CUIToSemanticType = {}
file4 = open("conceptSemanticType2019AB.csv","r")
#The content for each row: CUI, semantic type
reader4 = csv.reader(file4)
for row4 in reader4:
    if semanticType.get(row4[2],"Default") == "Default":
        semanticType[row4[2]] = [row4[0]]
    else:
        semanticType[row4[2]].append(row4[0])
    if CUIToSemanticType.get(row4[0],"Default") == "Default":
        CUIToSemanticType[row4[0]] = [row4[2]]
    else:
        CUIToSemanticType[row4[0]].append(row4[2])
file4.close()
#
ConceptNameGroup = sorted(list(nameStringToAUI_Original.keys()))
#test case
#ConceptNameGroup = ["accidental poisoning by butyrophenone-based tranquilizer","acquired arteriovenous fistula","entire head of proximal phalanx of thumb"]
output = open("potentialMissingIS-A_2ndRevision_NormalizedForToken.csv","w")
missingISAWriter = csv.writer(output)
for iii in range(0,len(ConceptNameGroup)): 
    print(iii)
    potentialChildAUIs = []  # a list of childAUI
    potentialParentAUIs = []  # a list of (parentAUI,parentAUIConceptName)          
    relatedAUICs = nameStringToAUI_Original.get(ConceptNameGroup[iii])
    for eachRelatedAUIC in relatedAUICs:
        if eachRelatedAUIC in allNodesInUMLSSet:
            potentialChildAUIs.append(eachRelatedAUIC)
    allCombinations = upperGenerator(ConceptNameGroup[iii])
    for eachComb in allCombinations[0]:
        newConceptName = " ".join(eachComb)
        if nameStrToAUI.get(newConceptName,"Default")!="Default":
            if allCombinations[2] == "PureSecondary":
                multipleReplacement = 1
            else:
                multipleReplacement = 0
                for i in range(len(eachComb)):
                    if eachComb[i] != allCombinations[3][i][0]:
                        multipleReplacement = multipleReplacement+1
            relatedAUIPs = nameStrToAUI.get(newConceptName)
            for eachRelatedAUIP in relatedAUIPs:
                if eachRelatedAUIP in allNodesInUMLSSet:
                    potentialParentAUIs.append((eachRelatedAUIP,newConceptName,multipleReplacement))
    if len(potentialParentAUIs)>0:
        potentialParentAUIs = list(set(potentialParentAUIs))
        for child in potentialChildAUIs:
            #childAncestors = set(findAncestors(child)) 
            #now we don't check if AUIP is already a parent/ancestor of AUIC
            #we make it to check how many detected cases are already included in current hierarchy (ground truth ones)
            for parent in potentialParentAUIs:
                #if child != parent[0] and parent[0] not in childAncestors and child not in set(findAncestors(parent[0])) and ConceptNameGroup[iii] != parent[1]:
                if child != parent[0] and ConceptNameGroup[iii] != parent[1]:
                    childSemantic = CUIToSemanticType.get(AUItoCUI.get(child)[0])
                    parentSemantic = CUIToSemanticType.get(AUItoCUI.get(parent[0])[0])
                    if set(childSemantic).issuperset(set(parentSemantic)):
                        missingISAWriter.writerow((AUItoNameStr.get(child)[0],parent[1],child,parent[0],str(allCombinations[1]),ConceptNameGroup[iii],parent[2]))
output.close()