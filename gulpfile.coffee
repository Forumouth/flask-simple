g = require "gulp"
notify = require "gulp-notify"
exec = require("child_process").exec
q = require "q"
g.task "test", ->
  nosetestsParams = [
    "--with-coverage"
    "--cover-erase"
    "--cover-package=flask_simple"
    "--all"
  ]
  shellCommands = [
    "echo 'Syntax Check'"
    "flake8 flask_simple tests"
    "echo 'Code Metrics check'"
    "radon cc -nc flask_simple tests"
    "echo 'Maintenancibility check'"
    "radon mi -nc flask_simple tests"
    "nosetests #{nosetestsParams.join " "} tests"
  ]
  if not process.env.CI
    shellCommands.splice 0, 0, ". ../bin/activate"
    shellCommands.push "deactivate"
  defer = q.defer()
  child = exec(shellCommands.join "&&")
  child.stdout.pipe process.stdout
  child.stderr.pipe process.stderr
  child.on "error", (error) ->
    notify.onError("<%= error.message %>")(error)
    defer.reject(error)
  child.on "close", (code, signal) ->
    errStr = "The command failed with "
    if code isnt null and code > 0
      codeErr = errStr + " code: #{code}"
      notify.onError("<%= error.message %>")(new Error codeErr)
      defer.reject codeErr
      return
    if signal isnt null
      codeErr = errStr + " signal: #{signal}"
      notify.onError("<%= error.message %>")(new Error codeErr)
      defer.reject codeErr
      return
    defer.resolve()
  defer.promise

g.task "default", ->
  g.watch [
    "flask_simple/**/*.py",
    "tests/**/*.py"
  ], ["test"]
