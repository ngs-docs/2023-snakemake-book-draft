# Never fail me - how to make shell commands always succeed

snakemake uses UNIX exit codes to determine if the shell command
succeeded; these are numeric values returned from the running
program. The value `0` (zero) indicates success, while any non-zero
value indicates error.


~~~admonish info title='How should we interpret UNIX exit codes?'

The UNIX "exit code" or "exit status" is a single number returned from
an exiting subprocess to the calling program. This is the way that a
shell or a workflow program receives information about the success or
failure of a subprogram that they executed.

A common default is that an exit code of 0 indicates success; this is
always true in POSIX systems like Linux and Mac OS X.  It is also
standardized by the GNU libc library on which many programs are built
(see link below).

In the bash shell for UNIX, the exit status from the previous command is
stored in the `$?` variable and you can evaluate it like so:
```shell
$ if [ $? -eq 0 ] ...
```
or you can use `&&` to only run a second command if the first command "succeeds" (exits with code 0):
```shell
$ program && echo success
```
and `||` to only run a second command if the first command fails (exits with a non-zero exit code):
```shell
$ program || echo failed
```

Why does zero indicate success? We haven't been able to track down an answer,
but if we had to guess, it's because 0 is a good singular value that stands
out!

To read more, see
[the Wikipedia entry on Exit status](https://en.wikipedia.org/wiki/Exit_status)
as well as the
[GNU libc manual section](https://www.gnu.org/software/libc/manual/html_node/Exit-Status.html).
~~~

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

You can ensure that a command in a `shell:` block never fails by
writing it like so:
```
shell command || true
```

This runs `shell command`, and then if the exit code is non-zero
(fail), it runs `true`, which always has an exit code of 0 (success)!

This is a bit dangerous - if the shell command fails, you won't know
except by reading the error message - but it's sometimes necessary!

Here's a simple snakemake example that demonstrates this approach by
trying to execute a script that doesn't exit! That command will always
fail, but the overall shell block will succeed anyway because we
use `|| true`:

```python
{{#include ../../code/misc/never-fail-me/never-fail-me.snakefile}}
```

(It also shows the peril of this approach, because this is probably a command
that should actually fail!)

CTB: mention subshells?
