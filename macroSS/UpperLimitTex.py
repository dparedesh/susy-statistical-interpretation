def tablefragment(m,tabname):

  tableline = ''

  tableline += '''
\\begin{table}
\\begin{center}
\\setlength{\\tabcolsep}{0.0pc}
\\begin{tabular*}{\\textwidth}{@{\\extracolsep{\\fill}}lcccc}
\\noalign{\\smallskip}\\hline\\noalign{\\smallskip}
{\\bf Signal channel}                        & $\\langle\\epsilon{\\rm \\sigma}\\rangle_{\\rm obs}^{95}$[fb]  &  $S_{\\rm obs}^{95}$  & $S_{\\rm exp}^{95}$ & $CL_{B}$ \\\\
\\noalign{\\smallskip}\\hline\\noalign{\\smallskip}
%%'''
## AK:  Commented OUT with p(s=0), old
## \\begin{table}
## \\begin{center}
## \\setlength{\\tabcolsep}{0.0pc}
## \\begin{tabular*}{\\textwidth}{@{\\extracolsep{\\fill}}lccccc}
## \\noalign{\\smallskip}\\hline\\noalign{\\smallskip}
## {\\bf Signal channel}                        & $\\langle\\epsilon{\\rm \\sigma}\\rangle_{\\rm obs}^{95}$[fb]  &  $S_{\\rm obs}^{95}$  & $S_{\\rm exp}^{95}$ & $CL_{B}$ & $p(s=0)$ \\\\

 # doAsym=False
  m_listofkeys = m.keys()
  m_listofkeys.sort()
  for name in m_listofkeys:
    tableline = addlinetosystable(tableline,m,name)

    
  tableline += '''
\\noalign{\\smallskip}\\hline\\noalign{\\smallskip}
\\end{tabular*}
\\end{center}
\\caption[Breakdown of upper limits.]{
95$\\%%$ CL upper limits on the visible cross-section ($\\langle\\epsilon\\sigma\\rangle_{\\rm obs}^{95}$) and on the observed  ($S_{\\rm obs}^{95}$ )  and expected ($S_{\\rm exp}^{95}$) number of signal events for the various signal regions.
%The last two columns indicate the CLB value and discovery p-value (p(s = 0)).
%%All numbers are given for the individual electron and muon channels.
The last two columns indicate the $CL_B$ value and discovery $p$-value ($p(s = 0)$). 
\\label{table.results.exclxsec.pval}}
\\end{table}
%%'''

  return tableline


def givetuplesym(m,name):
  #  ntuple = ( m[name][0][0], m[name][0][1], m[name][0][2], m[name][0][3] , m[name][0][4], m[name][0][5], m[name][0][6], m[name][0][7], m[name][0][8]) ## AK:  Commented OUT with p(s=0), old
  ntuple = ( m[name][0][0], m[name][0][1], m[name][0][2], m[name][0][3] , m[name][0][4], m[name][0][5])
  return ntuple

def addlinetosystable(tableline,m,name):
  try:
    m.has_key(name)
  except:
    print " \n", name, "  not inside the upper limit table"
    return tableline

  printname = name
  printname = printname.replace('_','\_')
  #    tableline += '\n'+ printname + '''   & $%.2f^{+%.2f}_{-%.2f}$ &  $%.1f$  & ${%.1f}^{+%.1f}_{-%.1f}$ & $%.2f$  &  $%.2f$ \\\\ ## AK:  Commented OUT with p(s=0), old
#  tableline += '\n'+ printname + '''   & $%.2f^{+%.2f}_{-%.2f}$ &  $%.1f$  & ${%.1f}^{+%.1f}_{-%.1f}$ & $%.2f$  \\\\
  tableline += '\n'+ printname + '''   & $%.2f$ &  $%.1f$  & ${%.1f}^{+%.1f}_{-%.1f}$ & $%.2f$  \\\\
  %%''' % givetuplesym(m,name)

  
  return tableline
 
