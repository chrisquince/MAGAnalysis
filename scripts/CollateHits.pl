#!/usr/bin/perl

my @hits = <*/*.hits>;
my %hashKO = {};
my $maxId = -1;
foreach my $file (@hits){
    #print "$file\n";

    if($file=~/Cluster(\d+)\/.*/){
        my $idx = $1;
        if($idx > $maxId){
            $maxId = $idx;
        }
        open(FILE,$file) or die "Can't open $file\n";

        while($line = <FILE>){
            chomp($line);
            my @tokens = split(/ /,$line);

            my $ko = $tokens[1];

            if($hashKO{$ko} eq undef){
                my @temp = ();
                $hashKO{$ko} = \@temp;
            }
            
            @{$hashKO{$ko}}[$idx]++;
        }
        close(FILE);
    }
}

my @cidx = ();
for(my $i = 0; $i <= $maxId; $i++){
    push(@cidx,"C${i}");
}
my $cstring = join(",",@cidx);
print "Clusters,${cstring}\n";

foreach my $kohit (sort {$a=~/ko:K(\d+)/; $ai = $1; $b=~/ko:K(\d+)/; $bi = $1; $ai <=> $bi;} keys %hashKO){
    my @hits = @{$hashKO{$kohit}};
    for(my $i = 0; $i <= $maxId; $i++){
        $hits[$i]++;
        $hits[$i]--;
    }
    my $hstring = join(",",@hits);
    print "$kohit,$hstring\n";
} 
