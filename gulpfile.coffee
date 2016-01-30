g = require "gulp"
notify = require "gulp-notify"
exec = require("child_process").exec
q = require "q"

g.task "test", ->
  shellCommands = [
    "echo 'Syntax Check'"
    "flake8 src tests"
    "echo 'Code Metrics check'"
    "radon cc -nc src tests"
    "echo 'Maintenancibility check'"
    "radon mi -nc src tests"
    "nosetests --all tests"
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
    "src/**/*.py",
    "tests/**/*.py"
  ], ["test"]
