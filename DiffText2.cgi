#! /usr/bin/perl -wT

#===================================================================
#     D I F F  T E X T  .  C G I
#===================================================================


#===================================================================
#     U S E  /  R E Q U I R E
#===================================================================
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use POSIX;
use FindBin;
my $path;
BEGIN { if ($FindBin::Bin =~ /(.*)/) { $path = $1; } }
use lib $path;
use strict;


#===================================================================
#     P R O T O T Y P E S
#===================================================================
sub getParams();
sub validateParams();
sub printIntroForm();
sub processData($$$);
sub getFileDiff($$);
sub processFileDiff($$);
sub getFileNames($);


#===================================================================
#    C O N F I G
#===================================================================
#my $HOME_URL = 'http://ec2-54-204-132-34.compute-1.amazonaws.com';
my $HOME_URL = 'http://www.aduprising.com';
my $HOME_DIR = '/usr/lib/cgi-bin/public';
my $THIS_SCRIPT = 'DiffText2.cgi';
my $DIFF = '/usr/bin/diff';
my $TEMP_DIR = '/tmp';


#===================================================================
#    G L O B A L S
#===================================================================
my $file1 = '';
my $file2 = '';


#===================================================================
#    P A R A M S
#===================================================================
my $mode = '';
my $text1 = '';
my $text2 = '';
my $test_name = '';


#===============================================================
#    M A I N
#===============================================================

#===== Untaint
$ENV{'PATH'} = '';

#===== Get Passed Parameters
getParams();

#===== Header stuff
printHeader();

#===== Body
print "<body>\n";

print "<h1>Diff Text Test</h1><br>\n";

#===== Get Passed Parameters
getParams();

if ($mode and $mode eq 'process_data')
{
  my $temp1 = '';
  my $temp2 = '';
  my $root1 = '';
  my $root2 = '';
  my $num_source_words = 0;

  if ($test_name)
  {
    my ($file1, $file2) = getFileNames($test_name);

    #===== Save file1 to a temp file
    my @fields1 = split("\/", $file1);
    $root1 = $fields1[@fields1-1];
    open(TXT, $file1) or die "Couldn't open file $file1 : $!\n";
    $text1 = join("", <TXT>);
    close(TXT);
    $num_source_words = scalar(split(' ', $text1));

    #===== Split so we have one word per line
    $text1 =~ s/ /\n/g;

    #===== Get the contents of file2
    my @fields2 = split("\/", $file2);
    $root2 = $fields2[@fields2-1];
    open(TXT, $file2) or die "Couldn't open file $file2 : $!\n";
    $text2 = join("", <TXT>);
    close(TXT);
   
    #===== Split so we have one word per line
    $text2 =~ s/ /\n/g;

  } # pre-configured test
  elsif ($text1 and $text2)
  {
    $text1 .= "\n";
    $text2 .= "\n";
  }

  if ($text1 and $text1)
  {
    #===== Init
    $root1 = 'pasted_text1.txt' unless $root1;
    $root2 = 'pasted_text2.txt' unless $root2;
    $num_source_words = scalar(split(' ', $text1));

    #===== Split so we have one word per line
    $text1 =~ s/ /\n/g;

    #===== Save to a temp file for processing
    $temp1 = "$TEMP_DIR/$root1";
    open(TEMP, ">$temp1") or die "Couldn't save temp file $temp1 : $!\n";
    print TEMP $text1; 
    close(TEMP);


    #===== Split so we have one word per line
    $text2 =~ s/ /\n/g;

    #===== Save this text to a temp file
    $temp2 = "$TEMP_DIR/$root2";
    open(TEMP, ">$temp2") or die "Couldn't save temp file $temp2 : $!\n";
    print TEMP $text2; 
    close(TEMP);
  }
  else
  {
    print "Must select a test or supply two text samples!\n";
  } 

  #===== Process the temp files
  processData($temp1, $temp2, $num_source_words);
}
else
{
  printIntroForm();
}

#===== Close body and HTML
print"</body>\n";
print "</html>\n";

exit;


############################### BEGIN SUBROUTINES ##############################


#==========================================================================
#    G E T  P A R A M S
#==========================================================================
sub getParams()
{
  if (param('mode')){ $mode = param('mode');}
  if (param('text1')){ $text1 = param('text1');}
  if (param('text2')){ $text2 = param('text2');}
  if (param('test_name')){ $test_name = param('test_name');} 

  return;

} # end of getParams()


sub printHeader()
{
  my $html = "";
  $html .= "\n<!DOCTYPE html>\n";
  $html .= "<html lang='en'>\n";
  $html .= "<head>\n";
  $html .= "<meta charset='utf-8' />\n";
  $html .= "<title>Diff Text Test</title>\n";
  $html .= "</head>\n";

  print $html;

}


#==========================================================================
#    P R I N T  I N T R O  F O R M
#==========================================================================
sub printIntroForm()
{

  #===== Form
  print "<form method='post' name='contact_form' action='$THIS_SCRIPT'>\n";

  #===== Form elements

  # Canned Tests
  print "Select a Pre-configured Test:<br>\n";
  print "<select name='test_name' id='test_name'>\n";
  print "<option value='' selected>Select a pre-configured test...</option>\n";
  print "<option value='text1-text1'>Text1 & Text 1</option>\n";
  print "<option value='text1-text2'>Text1 & Text2</option>\n";
  print "<option value='text1-text3'>Text1 & Text3</option>\n";
  print "<option value='text1-text4'>Text1 & Text4</option>\n";
  print "</select>\n";
  print "<p></p>\n";

  print "OR copy/paste text to be compared.\n";
  print "<p></p>\n";

  # Text 1
  print "First Text Field:<br>\n";
  print "<textarea rows='6' cols='40' id='text1' ";
  print "name='text1' placeholder='Source Text Goes Here'></textarea>\n";
  print "<p></p>\n";

  # Text 2
  print "Second Text Field:<br>\n";
  print "<textarea rows='6' cols='40' id='text2' ";
  print "name='text2' placeholder='Comparison Text Goes Here'></textarea>\n";
  print "<p></p>\n";

  # Submit Button
  print "<input type='submit' id='submit_btn' value='Submit'>\n";
  print "<input type='hidden' name='mode' value='process_data'>\n";

  #===== Close Form
  print "</form>\n";

  return;

} # end of printIntroForm()


#==========================================================================
#    P R O C E S S  D A T A
#==========================================================================
sub processData($$$)
{
  my $temp1 = shift or
    die "Must supply temp1 to processData()!\n";
  my $temp2 = shift or
    die "Must supply temp2 to processData()!\n";
  my $num_source_words = shift or
    die "Must supply num_source_words to processData()!\n";

  #===== Get the file diff
  my @lines = getFileDiff($temp1, $temp2);

  #===== Process the file diff
  my $diff_output = join("", @lines);
  my $coeff = processFileDiff(\@lines, $num_source_words);

  #===== Print results
  print "Source file has $num_source_words words.<br>\n";
  print "Match coefficient: $coeff<br>\n";

  #===== Debug
  $diff_output = 'none' unless $diff_output;
  print "Diff output:<br>\n";
  print "<pre>\n";
  print $diff_output;
  print "</pre>\n";

  return;

} # end of processData()


#==============================================================================
#    G E T  F I L E  D I F F
#
#    Arg1: The source file.
#    Arg2: The dest file.
#    Returns: An array of lines that result from diffing the two files.
#==============================================================================
sub getFileDiff($$)
{
  my $file1 = shift or 
    die "Must supply file1 to getFileDiff()!\n";
  my $file2 = shift or 
    die "Must supply file2 to getFileDiff()!\n";
  my @lines = ();

  #===== Build the diff command
  my $cmd = "$DIFF $file1 $file2";

  #===== Run the diff command
  if (open(CMD, "$cmd|"))
  {
    #===== Get the command output
    @lines = <CMD>;
    close(CMD);
  }
  else
  {
    #===== Let the user know we couldn't continue and why
    warn "Unable to run command $cmd : $!\n";
  }

  return(@lines);

} # end of getFileDiff()


#==============================================================================
#    P R O C E S S  F I L E  D I F F
#
#    Arg1: The lines from the diff output.
#    Arg2: The number of words in the source file.
#==============================================================================
sub processFileDiff($$)
{
  my $lines = shift or
    die "Must supply array ref to processFileDiff()!\n";
  my $num_source_words = shift or
    die "Must supply num_source_words to processFileDiff()!\n";

  my $source = 1;
  my $s_add = 0;
  my $s_subt = 0;
  my $d_add = 0;

  #===== Init the line score
  my $line_score = $num_source_words;

  #===== Process each line of output
  while (my $line = shift(@$lines))
  {
    if ($line =~ m/^</)
    {
      if ($source) { $s_subt++; }
    }
    elsif ($line =~ m/^>/)
    {
      $source ? $s_add++ : $d_add++;
    }
    elsif ($line =~ m/---/)
    {
      $source = 0;
    }
    else
    {
      #===== Reset
      $source = 1;
    }
  }

  $line_score -= $s_subt;
  if ($d_add > $s_subt)
  {
    $num_source_words += ($d_add - $s_subt);
  }


  my $coeff = $line_score/$num_source_words;  

  return($coeff);

} # end of processDiffFile()

sub getFileNames($)
{
  my $test_name = shift or
    die "Must supply test_name to getFileNames()!\n";

  if ($test_name)
  {
    if ($test_name eq 'text1-text1')
    {
      $file1 = 'text1.txt';
      $file2 = 'text1.txt';
    }
    elsif ($test_name eq 'text1-text2')
    {
      $file1 = 'text1.txt';
      $file2 = 'text2.txt';
    }
    elsif ($test_name eq 'text1-text3')
    {
      $file1 = 'text1.txt';
      $file2 = 'text3.txt';
    }
    elsif ($test_name eq 'text1-text4')
    {
      $file1 = 'text1.txt';
      $file2 = 'text4.txt';
    }
  }

  return($file1, $file2);

} # end of getFileNames()
