#### this should go into sitecustomize.py ####
import sys, os, subprocess
import ast, builtins

from xalt_python_pkg_filter import keep_pkg

if sys.version_info[0] >= 3:
  string_types = str,
else:
  string_types = basestring,

class RecorderRTM(object):
  """
  Record all requests to load a module by name.
  """
  __slots__ = ['_cmd','_keepT', '_declared']


  def __init__(self, uuid, version_str):
    self._cmd     = False
    self._keepT   = {}
    xaltDir       = os.environ.get("XALT_DIR")
    if (xaltDir):
      self._cmd     = "XALT_EXECUTABLE_TRACKING=no " + os.path.join(xaltDir,"libexec/xalt_record_pkg") + \
                      " -u " + uuid + " program python xalt_run_uuid " + uuid + " package_version " + version_str

      
    self._declared = set()
    user_script = os.path.realpath(sys.argv[0]) if sys.argv else None
    if user_script and os.path.isfile(user_script):
      try:
        with open(user_script, 'r') as f:
          self._declared |= self._roots_from_source(f.read())
      except Exception:
        pass
    # Interactive / python -c: parse each compiled snippet
    # Use a local (not self._orig_compile) — __slots__ would reject that attribute
    orig_compile = builtins.compile
    def _compile(source, filename, mode, *args, **kwargs):
      if filename in ('<stdin>', '<string>', '<console>', '<input>'):
        src = source.decode() if isinstance(source, (bytes, bytearray)) else source
        if isinstance(src, str):
          self._declared |= self._roots_from_source(src)
      return orig_compile(source, filename, mode, *args, **kwargs)
    builtins.compile = _compile
    
  def __keep(self, fullname, path):
    keepT              = self._keepT
    keep, reason, kind = keep_pkg(fullname, path)
    if (not keep):
      return False

    if (fullname in keepT):
      return False
    keepT[fullname] = True
    return True

  def __report(self, fullname, path):
    if (not self._cmd):
      return
    nonStrCount = 0
    if (not isinstance(fullname,string_types)):
      fullname = "'<unknown>'"
      nonStrCount = nonStrCount+1
    if (not isinstance(path,string_types)):
      path = "'<unknown>'"
      nonStrCount = nonStrCount+1
    if (nonStrCount >= 2):
      return
    os.environ['LD_PRELOAD'] = ""
    cmd = self._cmd + " package_name " + fullname + " package_path " + path
    subprocess.call(cmd, shell=True)

#   def _is_direct_user_import(self):
#     user_script = os.path.realpath(sys.argv[0]) if sys.argv else None
#     if user_script and not os.path.isfile(user_script):
#       user_script = None
#     for frame in inspect.stack()[2:]:
#       fn = frame.filename
#       # Interactive REPL / python -c
#       if fn in ("<stdin>", "<string>", "<console>"):
#         return True
#       if fn.startswith("<"):
#         continue
#       real = os.path.realpath(fn)
#       if user_script and real == user_script:
#         return True
#       if "site-packages" in real or "/lib/python" in real:
#         return False
#       if real.endswith(".py") and not real.startswith("/usr/"):
#         return True
#     return False

  
  def _roots_from_source(self, src):
    roots = set()
    try:
      tree = ast.parse(src)
    except Exception:
      return roots
    for node in ast.walk(tree):
      if isinstance(node, ast.Import):
        for alias in node.names:
          roots.add(alias.name.split('.')[0])
      elif isinstance(node, ast.ImportFrom):
        if node.level == 0 and node.module:
          roots.add(node.module.split('.')[0])
    return roots

  def _is_declared_import(self, fullname):
    if not fullname or not isinstance(fullname, string_types):
      return False
    return fullname.split('.')[0] in self._declared
  
  
  # Python 3.4+
  def find_spec(self, fullname, path, target=None):

    result = None
    for entry in sys.meta_path:
      cls  = type(entry)
      if (cls.__name__ != "RecorderRTM" ):
        try: 
          result = entry.find_spec(fullname, path, target)
        except:
          pass
        if (result):
          break

    if (not result):
      return result

    path = result.origin

    # if (self.__keep(fullname, path)):
    #   self.__report(fullname, path)
    
    # if (self.__keep(fullname, path) and self._is_direct_user_import()):
    #   self.__report(fullname, path)
    
    
    if (self.__keep(fullname, path) and self._is_declared_import(fullname)):
      self.__report(fullname, path)

    return result

  # Python 2.3--3.3
  def find_module(self, fullname, path):
    result = None
    path   = None

    for entry in sys.meta_path:
      cls  = type(entry)
      if (cls.__name__ != "RecorderRTM" ):
        result = entry.find_module(fullname, path)
        if (result):
          path = result.origin
          break
  
    for entry in sys.path:
      base = os.path.join(entry,fullname)
      fn   = base + ".py"
      if (os.path.exists(fn)):
        path = fn
        break
      else:
        fn   = os.path.join(base, "__init__.py")
        if (os.path.exists(fn)):
          path = fn
          break

    if (path and  self.__keep(fullname, path)):
      self.__report(fullname, path)

    return result




uuid        = os.environ.get("XALT_RUN_UUID",None)
if (uuid):
  sA = []
  for i in sys.version_info:
    s = str(i)
    if (s == 'final'):
      break
    sA.append(s)
  version_str = '.'.join(sA)

  sys.meta_path.insert(0, RecorderRTM(uuid, version_str))

