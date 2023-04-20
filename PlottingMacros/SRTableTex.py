def tableStart():
    Start = ''' 
\\begin{table}[htb!]
\\begin{center}
    '''
    return Start

def tabularStartAsym(ncol):
    col=''

    for i in range(ncol):
        col+=" r@{$^{+}_{-}$}l "

    tabStart = '''
\\small
\\begin{tabular}{l%s}
\\noalign{\\smallskip}\\hline\\hline\\noalign{\\smallskip}
    ''' % (col)
    return tabStart


def tabularStart(ncol):
    col=''

    for i in range(ncol):
	col+="c"
    
    tabStart = '''

\\setlength{\\tabcolsep}{0.0pc}{
\\small
\\begin{tabular*}{\\textwidth}{@{\\extracolsep{\\fill}}l%s}
\\noalign{\\smallskip}\\hline\\hline\\noalign{\\smallskip}
    ''' % (col)
    return tabStart


def tabularEndAsym():
    tabEnd = ''' 
\\noalign{\\smallskip}\\hline\\hline\\noalign{\\smallskip}
\\end{tabular}
    
    '''
    return tabEnd

def tabularEnd():
    tabEnd = '''
\\noalign{\\smallskip}\\hline\\hline\\noalign{\\smallskip}
\\end{tabular*}

}
    '''


    return tabEnd

def tableEnd(label,luminosity,VR,veto):
    extra=' '
    region_label=' signal ' 

    if VR:
        region_label=' validation '

    if veto:
        extra=' Background categories shown as ``$-$\'\' denote that they cannot contribute to a given region. '
     

    End = '''
\\end{center}
\\caption{The number of observed data events and expected background contributions in the %s regions for an integrated 
luminosity of \\SI{%s}{fb^{-1}}.''' % (region_label,luminosity)

    End+=extra

    End+='''The displayed yields include all sources of statistical and systematic uncertainties. The individual uncertainties can be correlated
and therefore do not necessarily add up in quadrature to the uncertainty on the total expected background.}
\\label{tab:%s}
\\end{table}
    ''' % (label)
    return End

def insertSingleLine():
    Line = '''
\\noalign{\\smallskip}\\hline\\noalign{\\smallskip}
    '''
    return Line

def insertDoubleLine():
    Line = '''
\\noalign{\\smallskip}\\hline\\hline\\noalign{\\smallskip}
    '''
    return Line


def insertSRnamesAsym(entries):

    endLine="    \\\[-0.05cm]"
    splitColumn="    &    "

    Line="\n"
    Line+= splitColumn

    for i in range(len(entries)):

        Line+="\\multicolumn{2}{c}{"+entries[i]+"}"

        if i==len(entries)-1:
            Line+=endLine
        else:
            Line+=splitColumn

    Line+="\n"

    return Line


def insertSRnames(entries):

    endLine="    \\\[-0.05cm]"
    splitColumn="    &    "

    Line="\n"
    Line+= splitColumn

    for i in range(len(entries)):

        Line+=entries[i]

        if i==len(entries)-1:
            Line+=endLine
        else:
            Line+=splitColumn

    Line+="\n"

    return Line

def insertObservedAsym(entries):
    Line = ''

    endLine="    \\\\"
    splitColumn="    &    "

    Line="\n"
    Line+= " Observed"+splitColumn

    for i in range(len(entries)):

        Line+="\\multicolumn{2}{c}{"+str(int(entries[i]))+"}"

        if i==len(entries)-1:
            Line+=endLine
        else:
            Line+=splitColumn


    Line+="\n"

    return Line

def insertObserved(entries):
    Line = ''

    endLine="    \\\\"
    splitColumn="    &    "

    Line="\n"
    Line+= " Observed"+splitColumn

    for i in range(len(entries)):

        Line+=str(int(entries[i]))

        if i==len(entries)-1:
            Line+=endLine
        else: 
            Line+=splitColumn
    
    
    Line+="\n"

    return Line

def insertTotalSMAsym(entries, errors_up,errors_dn):
    Line = ''

    endLine="    \\hspace*{1.95mm}  \\\\"
    splitColumn="    &    "

    Line="\n"
    Line+=" Total SM background"+splitColumn

    for i in range(len(entries)):

        val=entries[i]
        err_up=errors_up[i]
        err_dn=errors_dn[i]

        if val-err_dn>=0:
            Line+=str(("%.2f" %val))+" & $^{"+str(("%.2f" %err_up))+"}_{"+str(("%.2f" %err_dn))+"}$"
        else:
            Line+=str(("%.2f" %val))+" & $^{"+str(("%.2f" %err_up))+"}_{"+str(("%.2f" %val))+"}$"

        if i==len(entries)-1:
            Line+=endLine
        else:
            Line+=splitColumn


    Line+="\n"

    return Line


def insertTotalSM(entries, errors):
    Line = ''

    endLine="    \\hspace*{1.95mm}  \\\\"
    splitColumn="    &    "
    
    Line="\n"
    Line+=" Total SM background"+splitColumn

    for i in range(len(entries)):

        val=entries[i]
        err=errors[i]

        if val-err>=0:
	    Line+=str(("%.2f" %val))+" $\\pm$ "+str(("%.2f" %err))
        else:
            Line+=str(("%.2f" %val))+"$^{+"+str(("%.2f" %err))+"}_{-"+str(("%.2f" %val))+"}$"

        if i==len(entries)-1:
            Line+=endLine
        else:
            Line+=splitColumn


    Line+="\n"

    return Line


def insertBkgAsym(name, entries, errors_up, errors_dn, veto):
    Line = ''

    endLine="    \\\\"
    splitColumn="    &    "

    Line="\n"
    Line+=name+" "+splitColumn

    for i in range(len(entries)):

        val=entries[i]
        err_up=errors_up[i]
        err_dn=errors_dn[i]

        if i in veto:
            Line+="\\multicolumn{2}{c}{$-$}"
        #elif val-err_dn>=0:
#            Line+=str(("%.2f" %val))+"& $^{"+str(("%.2f" %err_up))+"}_{"+str(("%.2f" %err_dn))+"}$"


        else:
            Line+=str(("%.2f" %val))+"& $^{"+str(("%.2f" %err_up))+"}_{"+str(("%.2f" %err_dn))+"}$"
#            print('WARNING -->  For sample '+name+": truncating uncertainty!")
        #    Line+=str(("%.2f" %val))+"& $^{"+str(("%.2f" %err_up))+"}_{"+str(("%.2f" %val))+"}$"

        if i==len(entries)-1:
            Line+=endLine
        else:
            Line+=splitColumn


    Line+="\n"


    return Line


def insertBkg(name, entries, errors,veto):
    Line = ''

    endLine="    \\\\"
    splitColumn="    &    "

    Line="\n"
    Line+=name+" "+splitColumn

    for i in range(len(entries)):

        val=entries[i]
        err=errors[i]

        if i in veto:
	    Line+="$-$"
        elif val-err>=0:
            Line+=str(("%.2f" %val))+" $\\pm$ "+str(("%.2f" %err))
        else:
	    print('WARNING -->  For sample '+name+": truncating uncertainty!")
            Line+=str(("%.2f" %val))+"$^{+"+str(("%.2f" %err))+"}_{-"+str(("%.2f" %val))+"}$"

        if i==len(entries)-1:
            Line+=endLine
        else:
            Line+=splitColumn


    Line+="\n"


    return Line
