void rootlogon()
{
  // Load ATLAS style
  gROOT->LoadMacro("PlottingMacros/atlasstyle-00-03-04/AtlasStyle.C");
  gROOT->ProcessLine("SetAtlasStyle()");
}
