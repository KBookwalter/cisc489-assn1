#!/usr/bin/env perl

use strict;
use warnings;

my @cmd = ("python3", "starter-code.py");

my @args;
if (defined ($ARGV[1])) {
    @args = ($ARGV[0], $ARGV[1]);
} else {
    @args = ($ARGV[0]);
}

system(@cmd, @args) == 0 or die "Python script returned error $?";
