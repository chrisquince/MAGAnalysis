#!/usr/bin/perl

use strict;

my $scgFile  = $ARGV[0];
my $fastaFile = $ARGV[1];
my $cogID    = $ARGV[2];

my $minPurity = 0.75;

my @pureClusters = ();

open(SCGFILE,  $scgFile) or die "Can't open $scgFile\n";

my $line = <SCGFILE>;
while(my $line = <SCGFILE>){
    chomp($line);

    my @tokens = split(/\t/,$line);

    my $cluster = shift(@tokens);
    shift(@tokens);shift(@tokens);
    my $count = 0;
    foreach my $scg(@tokens){
        if($scg == 1){
            $count++;
        }
    }

    my $purity = $count/36;
    if($purity > $minPurity){
        push(@pureClusters,"Cluster${cluster}");
    }
   
}

close(SCGFILE);

my @Seq = ();
my @id       = ();
my %hashID   = {};
my $count = 0;

open(FILE, $fastaFile) or die "Can't open $fastaFile\n";

my $seq = "";

while($line = <FILE>){
    chomp($line);

    if($line =~ />(\S+) .*/){

    $id[$count] = $1;
    $hashID{$1} = $count;

    if($seq ne ""){
        $Seq[$count - 1] = $seq;

        $seq = "";
    }

    $count++;
    }
    else{
         $seq .= $line;
    }
}

$Seq[$count - 1] = $seq;
my $total = $count;

foreach my $cluster(@pureClusters){
    my $clusterFile = "${cluster}/${cluster}.cog";
    open(FILE,$clusterFile) or die "Can't open cluster file $clusterFile\n";
    my $idx = 0;
    while($line = <FILE>){
        chomp($line);

        my @tokens = split(/,/,$line);

        my $id = $tokens[0];
        my $cog = $tokens[1];

        if($cog eq $cogID){
            if(length($Seq[$hashID{$id}]) > 50 && $idx == 0){
                print ">${cluster}\n";
                print "$Seq[$hashID{$id}]\n";
                $idx++;
            }
        } 
    }

    close(FILE);
}
