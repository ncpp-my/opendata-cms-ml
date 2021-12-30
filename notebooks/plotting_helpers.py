import collections, ROOT

class MyDict(collections.OrderedDict):
  """
  Create an infinitely recursive dictionary that can be self filled in runtime
  """
  def __missing__(self, key):
    val = self[key] = MyDict()
    return val

def FormatAxisText(histo, xTitle=None, yTitle=None, yOffset=0.3, xOffset=1.1):
  """
  Format the axis labels manually as TDRStyle seems unable to work properly
  args:
    histo = TH object whose axes need to be formatted
    xTitle = label of the x-axis
    yTitle = label of the y-axis
    yOffset, xOffset = how far the label will be from the axes 
  """


  if xTitle is not None:
    histo.GetXaxis().SetTitle(xTitle)

  if yTitle is not None:
    histo.GetYaxis().SetTitle(yTitle)

  histo.GetXaxis().SetLabelSize(0.035)
  histo.GetYaxis().SetLabelSize(0.035)
  histo.GetXaxis().SetTitleSize(0.04)
  histo.GetYaxis().SetTitleSize(0.04)
  histo.GetXaxis().SetTitleOffset(xOffset)
  histo.GetYaxis().SetTitleOffset(yOffset)

def SetSignalBackgroundDotStyle(sig, bgd):
  """
  For plotting KS-test plots, formatting the histograms from training to be disitnct from the testing ones
  args:
    sig = signal histogram
    bgd = background histogram
  """

  bgd.SetMarkerColor(ROOT.kRed+2)
  bgd.SetMarkerSize( 0.7 )
  bgd.SetMarkerStyle( 20 )
  bgd.SetLineWidth( 1 )
  bgd.SetLineColor(ROOT.kRed+2)
 
  sig.SetMarkerColor(ROOT.kBlue+2)
  sig.SetMarkerSize( 0.7 )
  sig.SetMarkerStyle( 20 )
  sig.SetLineWidth( 1 )
  sig.SetLineColor(ROOT.kBlue+2)

def SetupFrame(sig, bkg, methodName):
  """
  Build a 2-D histogram to act as a frame for the TMVA plots
  args:
    sig = signal histogram
    bkg = background histogram
    methodName = name of TMVA method
  """

  ymin, nrms, nb = 0, 10, 500
  ymax = max( sig.GetMaximum(), bkg.GetMaximum())*1.25
  xmin = max( min(sig.GetMean() - nrms*sig.GetRMS(), bkg.GetMean() - nrms*bkg.GetRMS()), sig.GetXaxis().GetXmin())
  xmax = min( max(sig.GetMean() + nrms*sig.GetRMS(), bkg.GetMean() + nrms*bkg.GetRMS()), sig.GetXaxis().GetXmax())
  
  frame = ROOT.TH2F("frame"+sig.GetName(), sig.GetTitle(), nb, xmin, xmax, nb, ymin, ymax)
  FormatAxisText(frame, xTitle=methodName+" response", yTitle="(1/N) dN^{ }/^{ }dx")

  return frame
