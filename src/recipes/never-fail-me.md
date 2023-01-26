# Never fail me - how to make shell commands always succeed

CTB: incomplete

CTB TODO: explain shell exit codes somewhere

Sometimes your shell commands will _need_ to fail, because of the way they
are constructed. For example, if you are using piping to truncate the
output of a command, UNIX will stop the command once the receiving end of
the pipe ceases to accept input. Look at this command to take only
the first 1,000,000 lines from a gzipped file:

```
gunzip -c large_file.gz | head -1000000 
```

If there are more than 1 million lines in `large_file.gz`, this command
will fail, because `head` will stop accepting input after 1 million lines
and gunzip will be unable to write to the pipe. 

CTB: add example error message.

Other situations where this arises is when you're using a script or
program that just doesn't exit with status code 0, for some reason
beyond your control.

You can ensure that your shell command never fails like so:
```
(shell command) || true
```

While this is dangerous, it's sometimes necessary!

CTB: provide snakefile example
