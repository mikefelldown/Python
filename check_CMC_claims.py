#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mfell
#
# Created:     27/04/2015
# Copyright:   (c) Canadian Malartic Corporation 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import urllib
import BeautifulSoup as bs


def main():
    params = 'HolderName=CANADIAN+MALARTIC+CORPORATION&txtDiv=80'
    request_url = 'http://www.mci.mndm.gov.on.ca/Claims/Cf_Claims/clm_clr.cfm'
    page = urllib.urlopen(request_url, params)
    soup = bs.BeautifulSoup(page.read())
    tab = soup.findAll("table")
    rows = tab.findAll("tr")
    claim_list = [row.find('a').getText() for row in rows[1:]]

if __name__ == '__main__':
    main()
