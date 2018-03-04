# Change Log

## v0.1.3

- Converted AD cmdlet to HyperV cmdlet

## v0.1.2

- Fixed `$ProgressPreference=false` by setting it to `$ProgressPreference = 'SilentlyContinue'`

  Contributed by Nick Maludy (Encore Technologies)

## v0.1.1

- In new versions of Powershell if you load a module some text is output into 
  the stream. Pywinrm doesn't handle this gracefully and it leaks into the 
  stderr (https://github.com/diyan/pywinrm/issues/169). This version fixes
  the issue by inserting `$ProgressPreference=false` at the beginning of the
  powershell script that's being run.
  
  Contributed by Brad Bishop (Encore Technologies) #1

## v0.1.0

Initial Revision
