

skulist = ['day','god','sah','tem']
barcodes={'day':'1','god':'2','sah':'3','tem':'4'}
bundleTiers = {}
bundleTiers = ['all','4 or more palettes','3 palettes', '2 palettes','2 palettes not temptress',\
               '2 palettes with temptress','1 palette']

bundleTiers = ['1 palette','2 palettes with mailer','2 palettes with envelope','3 palettes','4 or more palettes','all']

itemMixCount={}
bundleCounts={}
packedOrders=[]
def bundleFit(itemMix,bundle):
    isBundle=True
    #print itemMix
    if bundle == '1 palette':
        if len(itemMix[3]) != 1:
            isBundle=False
    elif bundle == '2 palettes with mailer':
        if len(itemMix[3]) !=2:
            isBundle=False
        if 'tem' not in str(itemMix[3]):
            isBundle=False
        if 'day' in str(itemMix[3]):
            isBundle=False
    elif bundle == '2 palettes with envelope':
        if len(itemMix[3]) !=2:
            isBundle=False
        if 'tem' in str(itemMix[3]):
            if 'day' not in str(itemMix[3]):
                isBundle=False
    elif bundle == '3 palettes':
        if len(itemMix[3]) !=3:
            isBundle=False
    elif bundle == '4 or more palettes':
        #print len(itemMix[3])
        if len(itemMix[3]) < 4:
            isBundle=False

    #print itemMix[3],isBundle,itemMix, len(itemMix[3])
    return isBundle
            
import datetime
 
# getting current date and time
d = datetime.datetime.today()

#add pages to item mixes

#bundleCountsCorrect=False
#while bundleCountsCorrect = False
    #loop through item mixes
        #if len(item mix > 2), continue
        
        #else if <3, add to most specific tier it fits in
            #loop through bundles
                #if it fits
                    #for order in itemMix:
                        #try:
                            #itemMixes[bundleName].append(order)
                        #except:
                            #itemMixes[bundleName]=[order]
                    #itemMixes.pop(itemMix)
    #bundleCountsCountsCorrect=True
    #for itemMix in itemMixes:
        #if len(itemMix < 3:
            #bundleCountsCountsCorrect=False

#for bundleCount in bundleCounts:
    #if

#for itemMix in itemMixes:
    #if len itemMix < 3:
        #for bundleCount in bundleCounts:
            #if bundleCount>2:
                #if it fits
                    #for order in itemMix:
                        #try:
                            #itemMixes[bundleName].append(order)
                        #except:
                            #itemMixes[bundleName]=[order]
                    #itemMixes.pop(itemMix)

packagingTypes={}
import ast
import time
#open main input file with all shipping records
import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
import operator
from collections import OrderedDict
infile=open("input "+str(d.month)+'-'+str(d.day)+".pdf", 'rb') 
reader = PdfFileReader(infile)
writer = PdfFileWriter()
numPages = reader.getNumPages()
read_pdf = PyPDF2.PdfFileReader(infile)
trackingNumbers = {}
orderNumbers=[]
packedTracking = []
bundles={}
trackingToOrder={}


######################################
#add page numbers and order info to bundles
######################################
for pageNum in range(numPages):
    #writer.addPage(reader.getPage(pageNum))
    page = read_pdf.getPage(pageNum)
    
    pageContent = page.extractText()
    if pageNum == 9:
        pass
   
    if 'PRICETOTAL' not in pageContent:
        continue
    orderNum = pageContent.split('Order Number:')[1].split('Order Date')[0].strip().lstrip()
    
    if orderNum not in orderNumbers and orderNum not in open('packedOrders.txt').read():
        orderNumbers.append(orderNum)
    else:
        raw_input('Error: duplicate order number, '+orderNum +\
                  'skipping this one, notify Bence\nPress ENTER to continue')
        continue

    trackingNumber = pageContent.split('Tracking:')[1].split('Packaging')[0].strip().lstrip()

    trackingToOrder[trackingNumber]=orderNum
    
    itemText = pageContent.split('PRICETOTAL')[1].split('Order Number')[0].encode('utf8')
    #print itemText
    itemMix=[]
    
    for sku in skulist:
        if sku in itemText:
            
            itemMix.append([itemText.split(sku)[0][-1],sku])
    try:
        bundles[str(itemMix)].append([pageNum,trackingNumber,orderNum,itemMix])
    except:
        bundles[str(itemMix)]=[[pageNum,trackingNumber,orderNum,itemMix]]

    
    if trackingNumber not in trackingNumbers:
        trackingNumbers[trackingNumber] = str(itemMix)
    else:
        raw_input('Error: duplicate tracking number, '+orderNum +\
                  'skipping this one, notify Bence\nPress ENTER to continue')
        continue

bundles= OrderedDict(sorted(bundles.items(), key=lambda x: len(x[1]),reverse=True))
   
#######################################
#smart combine bundles with low counts
#######################################
#print bundles
bundleCountsCorrect=False
done=False
while bundleCountsCorrect == False:
    for bundle in bundles:
        #print bundle

        if len(bundles[bundle])>=3:
            continue
        elif len(bundles[bundle])<3:

            lastorder=''
            print bundle
            print bundles[bundle]
            for order in bundles[bundle]:
                
                pastCurrentBundle=False
                
                for bundleTier in bundleTiers:
                    print bundleTier
                    if bundleTier == 'all':
                        pastCurrentBundle=True
                    elif bundle in bundleTiers:
                        if bundle == bundleTiers:
                            pastCurrentBundle=True
                            continue
                    else:
                        pastCurrentBundle=True
                    if not pastCurrentBundle:
                        continue
                    if bundleFit(order,bundleTier) == True:
                        #print order
                        try:
                            if order in bundles[bundleTier]:
                                lastorder=order
                                done=True
                                break
                        except:
                            pass
                        try:
                            
                            bundles[bundleTier].append(order)
                        except:
                            bundles[bundleTier]=[order]
                        print 'new bundle', bundleTier
                        print bundles[bundleTier]
                        lastorder=order
                        break
                    #print bundles[bundle]
            #print bundle
           #print ''
            #print bundles
            #print ''
            if not done:
                bundles.pop(bundle)
 
    bundleCountsCorrect=True

    for bundle in bundles:
        print len(bundles[bundle])
        if len(bundles[bundle])<3:

            if bundle != 'all':
                bundleCountsCorrect=False

for bundle in bundles:
    print bundle, bundles[bundle]
    print ''

        #if len(item mix > 2), continue
        
        #else if <3, add to most specific tier it fits in
            #loop through bundles
                #if it fits
                    #for order in itemMix:
                        #try:
                            #itemMixes[bundleName].append(order)
                        #except:
                            #itemMixes[bundleName]=[order]
                    #itemMixes.pop(itemMix)
    #bundleCountsCountsCorrect=True
    #for itemMix in itemMixes:
        #if len(itemMix < 3:
            #bundleCountsCountsCorrect=False

totalOrders=0
writer = PdfFileWriter()

#######################################
#print total orders and total of each item mix
#######################################
for bundle in bundles:
    totalOrders+=len(bundles[bundle])
print '_______________________________'
print totalOrders,'Total Orders'
print '__________'
for bundle in bundles:
    for pageNum in bundles[bundle]:
        filename=''
        try:
            for itemStr in ast.literal_eval(bundle):
                for element in itemStr:
                    filename+=element
                filename+=','
            filename=filename[:-1]
        except:
            filename = bundle
    print len(bundles[bundle]),'('+filename+')'

print '_______________________________'

#######################################
#start pick and pack
#######################################
import os
totalPacked=0
for bundle in bundles:
    writers=[]
    writers.append(PdfFileWriter())
    pageCount=0
    writerCount=0
    bundlePacked=0

    #get packaging type:
    print bundle
    if len(bundle) == 1:
        if 'day' in str(bundle):
            packagingType = 'Mailer'
    
    if totalPacked>0:
        print '\n'*20
        print 'Total Packed: '+str(totalPacked) +' out of '+str(totalOrders)
    for pageNum in bundles[bundle]:
        pageNum = pageNum[0]
        
        #print pageNum
        if pageCount>100:
            writerCount+=1
            pageCount=0
        writers[writerCount].addPage(reader.getPage(pageNum-1))
        writers[writerCount].addPage(reader.getPage(pageNum))
        filename=''

        try:
            for itemStr in ast.literal_eval(bundle):
                for element in itemStr:
                    filename+=element
                filename+=','
            filename=filename[:-1]
        except:
            filename = bundle
        pageCount+=1
    
    for writer in writers:
        print '_______________________________'
        print 'Print box label, place on an empty box'
        #time.sleep(1.5)
        open('boxlabel.txt','w').write(str(len(bundles[bundle]))+' ('+filename+')')
        os.system('boxlabel.txt')
        print '\n'*20
        print 'Print and gather:'
        #print len(bundles[bundle]),'('+filename+')'
        print '_______'
        items={}
        for order in bundles[bundle]:
            for item in order[3]:
                try:
                    items[item[1]]+=int(item[0])
                except:
                    items[item[1]]=int(item[0])
        for item in items:
            print items[item], item
        print '_______'
        #time.sleep(1.5)
        with open(filename.replace(',','').replace(' ','')+'.pdf', 'wb') as outfile:
            writer.write(outfile)
        os.system(filename.replace(',','').replace(' ','')+'.pdf')
        packed=0

        time.sleep(1)
        while packed < writer.getNumPages() /2:
            print '\n'*20
            
            print '('+filename+")'s packed: "+ str(bundlePacked) +' out of '+str(len(bundles[bundle]))
            trackingNumber = raw_input('Scan Label:\n')
            trackingNotCorrect=True
            while trackingNotCorrect:
                if len(trackingNumber) != len('9400111298370650356198'):
                    trackingNumber = raw_input('Length of tracking number not correct, try again:\n')
                    continue
                
                if trackingNumber in packedTracking:
                    trackingNumber = raw_input('Order already packed: double check then scan next label:\n')
                    continue
                if trackingNumber not in str(bundles[bundle]): #only checks from all of item mix, not the batch
                    trackingNumber = raw_input('Tracking number not found, try again:\n')
                    continue
                trackingNotCorrect=False
                    
            prepacked=False
            for item in ast.literal_eval(trackingNumbers[trackingNumber]):
                if prepacked:
                    break
                itemStr=''
                for x in range(int(item[0])):
                    barcode = raw_input('Scan '+ item[1]+'\n')
                    while barcode != barcodes[item[1]]:
                        if barcode =='':
                            print '_________________'
                            print 'Prepacked box used'
                            print '_________________'
                            print ''
                            prepacked=True
                            break
        
                    barcode = raw_input('wrong barcode, try again:\n')
            trackingNumberPacked = raw_input('Scan label again after packing and labeling:\n')
            while trackingNumberPacked !=trackingNumber: #only checks from all of item mix, not the batch
                
                trackingNumberPacked = raw_input('Wrong label, try again:\n')
            packedTracking.append(trackingNumberPacked)
            packed+=1
            totalPacked+=1
            bundlePacked+=1
            packedOrders.append(trackingToOrder[trackingNumber])
            open('packedOrders.txt','a').write(str(trackingToOrder[trackingNumber])+'\n')


print '\n'*20
print 'Total Packed: '+str(totalPacked) +' out of '+str(totalOrders)
#loop through all records
#loop through all files and put file numbers in each of the same item mix in their respective dictionary bin {[item mix]:[[pageNumbers],pakaging typ]}
#if bins have too few items do intelligent combining, same type of pakaging
#verify that total order number is correct
#loop through each dictionary type in order of most orders
    #open text doc with text of order type and number of that order to stick on box
    #create and open the pdf file for the packer to print 
    #print items they should gather
    #allow scans
    
#grab each product type and save to it's individual product type pdf, product type list [[orderNumbers],packagingtype,
#and add to all product list [[orderNumbers
