#! /usr/bin/perl -w

#===== Use / Require
use strict;

#===== Config
my $DIFF = '/usr/bin/diff';
my $TEMP_DIR = '/tmp';

#===== Prototypes
sub writeTempFiles($$);
sub getFileDiff($$);
sub countFileWords($);
sub processFileDiff($$);

#===== Get the text files to compare
my $file1 = $ARGV[0] or die "Must supply first file for comparison!\n";
my $file2 = $ARGV[1] or die "Must supply first file for comparison!\n";

#===== Get the words in the source file
my $num_source_words = countFileWords($file1);
my $num_dest_words = countFileWords($file2);

#===== Get the file diff
my @lines = getFileDiff($file1, $file2);

#===== Debug
print join("", @lines);

#===== Process the file diff
my $coeff = processFileDiff(\@lines, $num_source_words);


exit;


###################### BEGIN SUBROUTINES ######################################


sub writeTempFiles($$)
{
  my $file1 = shift or 
    die "Must supply file1 to getFileDiff()!\n";
  my $file2 = shift or 
    die "Must supply file2 to getFileDiff()!\n";
  my @temp_files = ();

  #===== Process text files
  foreach my $file ($file1, $file2)
  {
    #===== Get the filename to use in saving a temp file
    my @fields = split("\/", $file);
    my $root = $fields[@fields-1];

    #===== Read in the file
    open(TXT, $file) or die "Couldn't open file $file : $!\n";
    my $body = join("", <TXT>);
    close(TXT);

    #===== Split into one-word-per-line
    $body =~ s/ /\n/g;
  
    #===== Save to /tmp for diffing
    print "Saving $root to /tmp for diffing...\n";
    open(TEMP, ">$TEMP_DIR/$root") or die "Couldn't save temp file $root : $!\n";
    print TEMP $body; 
    close(TEMP);
    push(@temp_files, "$TEMP_DIR/$root"); 
  }

  
  return(@temp_files);

} # end of writeTempFiles()


sub getFileDiff($$)
{
  my $file1 = shift or 
    die "Must supply file1 to getFileDiff()!\n";
  my $file2 = shift or 
    die "Must supply file2 to getFileDiff()!\n";
  my @lines = ();

  #===== Write contents to the temp directory
  my @temp_files = writeTempFiles($file1, $file2);

  #===== Build the diff command
  my $cmd = "$DIFF " . join(" ", @temp_files);

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
#    C O U N T  F I L E  W O R D S
#
#    Arg1: The full path to the file we're getting a word count for.
#    Returns: The number of words found.
#==============================================================================
sub countFileWords($)
{
  my $file = shift or
    die "Must supply file to countFileWords()!\n";
  my $count = 0;

  #===== Read in the file
  open(TXT, $file) or die "Couldn't open file $file : $!\n";
  my $body = join("", <TXT>);
  close(TXT);
  $count = scalar(split(' ', $body));
  print "File $file contains $count words.\n";

  return($count);

} # end of countFileWords()


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
  my $changes = 0;
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
  print "Coeff: $coeff\n";

  return($coeff);

} # end of processDiffFile()
