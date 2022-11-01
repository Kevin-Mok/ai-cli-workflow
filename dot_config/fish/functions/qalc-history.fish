function qalc-history
    qalc $argv[1] | tee -a /home/example/Documents/journal/personal/calc-history.md
end
