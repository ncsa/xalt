from typing import List, Dict, Tuple
from datetime import datetime

class PkgObj():
#  def __init__(self, data, path):
  def __init__(self, data):
#      self.path = path
      self.xalt_run_uuid = data.get('xalt_run_uuid')
      self.pkg_version = data.get('package_version')
      self.pkg_name = data.get('package_name')
      self.pkg_path = data.get('package_path')
#      self.pkg_version = data.get('pkg_version')
#      self.pkg_name = data.get('pkg_name')
#      self.pkg_path = data.get('pkg_path')
  def writeToDB(self, conn):
    """
    Write new package data to the database using provided MariaDB connection.
    Uses xalt_run_uuid directly as run_id and 'python' as program.
    
    Args:
        conn: MariaDB connection object
    
    Returns:
        pkg_id: The ID of the inserted package record
    """
    print(f"run UUID:{self.xalt_run_uuid}")
    print(f"package name:{self.pkg_name}")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO xalt_pkg 
            (run_uuid, program, pkg_name, pkg_version, pkg_path)
            VALUES (%s, 'python', %s, %s, %s)
        """, (
#            int(self.xalt_run_uuid),  # Ensure run_id is an integer since it's int(11)
            self.xalt_run_uuid,  # Craig removed int() of this value
            self.pkg_name,       # Respect varchar(64) limit
            self.pkg_version if self.pkg_version else None,  # Respect varchar(32) limit
            self.pkg_path if self.pkg_path else None      # Respect varchar(1024) limit
#            self.pkg_name[:64],       # Respect varchar(64) limit
#            self.pkg_version[:32] if self.pkg_version else None,  # Respect varchar(32) limit
#            self.pkg_path[:1024] if self.pkg_path else None      # Respect varchar(1024) limit
        ))
        
        pkg_id = cursor.lastrowid
        conn.commit()
        
        return pkg_id
        
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error writing package to database: {str(e)}")
    finally:
        cursor.close()
     
     
class LinkObj:
  def __init__(self, json_data: dict, path):
      self.path = path
      resultT = json_data["resultT"]  # Direct access since the field is guaranteed to exist
      print(resultT)
      self.xalt_run_uuid = resultT["uuid"]
      self.crc = json_data["crc"]

      # Extract resultT fields


      self.link_program = resultT["link_program"]
      self.link_path = resultT["link_path"]
      self.build_user = resultT["build_user"]
      self.build_epoch = resultT["build_epoch"]
      self.exec_path = resultT["exec_path"]
      self.hash_id = resultT["hash_id"]
      self.wd = resultT["wd"]
      self.build_syshost = resultT["build_syshost"]

      # Extract linkA, function, and link_line fields
      self.linkA = json_data["linkA"]
      self.function = json_data["function"]
      self.link_line = json_data["link_line"]

  def __repr__(self):
      return (f"LinkObj(xalt_run_uuid={self.xalt_run_uuid}, crc={self.crc}, link_program={self.link_program}, "
              f"link_path={self.link_path}, build_user={self.build_user}, build_epoch={self.build_epoch}, "
              f"exec_path={self.exec_path}, hash_id={self.hash_id}, wd={self.wd}, build_syshost={self.build_syshost}, "
              f"linkA={self.linkA}, function={self.function}, link_line={self.link_line})")
  def writeToDB(self, conn):
    """
    Write link data to the database using provided MariaDB connection.
    Uses xalt_run_uuid directly as uuid and respects the column constraints.

    Args:
        conn: MariaDB connection object
    
    Returns:
        link_id: The ID of the inserted link record
    """
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO links 
            (hash_id, date, link_program, link_path, link_module_name,
             link_line, cwd, build_user, build_syshost, build_epoch,
             exec_path, uuid)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            self.hash_id[:40],                # Ensure hash_id is 40 chars (char(40))
            # datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Current timestamp for date
            self.link_program[:64],           # Respect varchar(64) limit for link_program
            self.link_path[:1024],            # Respect varchar(1024) limit for link_path
            self.linkA[:64] if self.linkA else None,  # Respect varchar(64) limit for link_module_name
            self.link_line,                   # link_line is a blob, can be passed as-is
            self.wd[:1024] if self.wd else None,  # Respect varchar(1024) limit for cwd
            self.build_user[:64],             # Respect varchar(64) limit for build_user
            self.build_syshost[:64],          # Respect varchar(64) limit for build_syshost
            self.build_epoch,                 # build_epoch is a double
            self.exec_path[:1024],            # Respect varchar(1024) limit for exec_path
            self.xalt_run_uuid                # uuid for the link record
        ))

        link_id = cursor.lastrowid  # Get the ID of the inserted link record
        conn.commit()  # Commit the transaction

        return link_id

    except Exception as e:
        conn.rollback()  # Rollback in case of error
        raise Exception(f"Error writing link to database: {str(e)}")

    finally:
      return      # Close the cursor after operation

class RunObj:
#  def __init__(self, json_data: dict, path):
  def __init__(self, json_data: dict):
      # Extract fields from the json_data dictionary
#      self.path = path
      self.crc = json_data.get("crc", "")
      self.cmdlineA = json_data.get("cmdlineA", [])
      self.hash_id = json_data.get("hash_id", "")
      
      # libA is a list of strings
      self.libA = json_data.get("libA", [])
      
      # ptA is a list of dictionaries with each dictionary having cmd_name, cmd_path, pid, and cmdlineA
      self.ptA = [
          {
              "cmd_name": pt.get("cmd_name", ""),
              "cmd_path": pt.get("cmd_path", ""),
              "pid": pt.get("pid", 0),
              "cmdlineA": pt.get("cmdlineA", [])
          }
          for pt in json_data.get("ptA", [])
      ]
      
      # envT is a dictionary of unlimited key-value pairs (environment variables)
      self.envT = json_data.get("envT", {})
      
      # userT is a dictionary with information about the user and job environment
      self.userT = {
          "syshost": json_data.get("userT", {}).get("syshost", ""),
          "run_uuid": json_data.get("userT", {}).get("run_uuid", ""),
          "exec_path": json_data.get("userT", {}).get("exec_path", ""),
          "exec_type": json_data.get("userT", {}).get("exec_type", ""),
          "cwd": json_data.get("userT", {}).get("cwd", ""),
          "currentEpoch": json_data.get("userT", {}).get("currentEpoch", ""),
          "start_date": json_data.get("userT", {}).get("start_date", ""),
          "user": json_data.get("userT", {}).get("user", ""),
          "execModify": json_data.get("userT", {}).get("execModify", ""),
          "scheduler": json_data.get("userT", {}).get("scheduler", ""),
          "account": json_data.get("userT", {}).get("account", ""),
          "job_id": json_data.get("userT", {}).get("job_id", ""),
          "queue": json_data.get("userT", {}).get("queue", ""),
          "submit_host": json_data.get("userT", {}).get("submit_host", "")
      }
      
      # userDT is a dictionary containing runtime and task-related data
      self.userDT = {
          "start_time": json_data.get("userDT", {}).get("start_time", 0.0),
          "end_time": json_data.get("userDT", {}).get("end_time", 0.0),
          "run_time": json_data.get("userDT", {}).get("run_time", 0.0),
          "probability": json_data.get("userDT", {}).get("probability", 1.0),
          "num_tasks": json_data.get("userDT", {}).get("num_tasks", 1.0),
          "num_gpus": json_data.get("userDT", {}).get("num_gpus", 0.0),
          "exec_epoch": json_data.get("userDT", {}).get("exec_epoch", 0.0),
          "num_threads": json_data.get("userDT", {}).get("num_threads", 1.0),
          "num_cores": json_data.get("userDT", {}).get("num_cores", 1.0),
          "num_nodes": json_data.get("userDT", {}).get("num_nodes", 1.0)
      }
      
      # XALT_measureT is a dictionary of measurement values for different steps in the process
      self.XALT_measureT = json_data.get("XALT_measureT", {})

      # XALT_qaT is a dictionary with QA-specific information
      self.XALT_qaT = json_data.get("XALT_qaT", {})
      self.xalt_run_uuid = self.userT['run_uuid']

      
  def __repr__(self):
      return (
          f"RunObj(crc={self.crc}, cmdlineA={self.cmdlineA}, hash_id={self.hash_id}, "
          f"libA={self.libA}, ptA={self.ptA}, envT={self.envT}, userT={self.userT}, "
          f"userDT={self.userDT}, XALT_measureT={self.XALT_measureT}, XALT_qaT={self.XALT_qaT})"
      )
  def writeToDB(self, conn):
    """
    structure copied from Prakhar's link object definition with mods for 
    minimal output testing 2026Feb
    """
    print('starting writetoDB() test')
    cursor = conn.cursor()
    #    try:
    #      cursor.execute("""
    #            INSERT INTO links
    #            (run_uuid,start_time,user,cwd,cmdline)
    #            VALUES (%s, %s, %s, %s, %s)
    #      """, (
    
    # test
    my_user=self.userT["user"]
    my_start_date=self.userT["start_date"]
    command_count=0
    print(f'user={my_user} date={my_start_date}')
    print('writeToDB test: about to output type')
    print(type(self.ptA))
    print(f'ptA length={len(self.ptA)}')
    print('writeToDB test: about to loop')
    #      for command_dict in self.ptA.blahblah:
    #        command_count += 1
    #        my_command=command_dict[cmd_name]
    #        print(f'Command {command_count} = {my_command}')
    
    print('finished looping')
    
    #      print('writetoDB for run test')
    
    #      return 0

    test_string=self.XALT_qaT["XALT_RESULT_FILE"]

    #    if test_string.contains(".aaa."):
    if ".aaa." in test_string:
      start_tag="aaa"
    else:
      start_tag=""
    
    cursor.execute("""
        INSERT INTO xalt_run
        (run_uuid,date,syshost,start_time,user,cwd,start_end)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
      self.userT["run_uuid"],
#      self.userT["start_date"],  # original;
      datetime.fromtimestamp(self.userDT["start_time"]).strftime('%Y-%m-%d %H:%M:%S'),  # Current timestamp for date
      self.userT["syshost"],
      self.userDT["start_time"],
      my_user,
      self.userT["cwd"],
      start_tag
    ))
#    ),use_pure=True)
    
    print('cursor ran; return value:{link_id}')
    link_id = cursor.lastrowid # new index just inserted
    conn.commit()
    print('commit() ran; returning from writeToDB()')
    
    return link_id

#    except Exception as e:
#      conn.rollback() # undo in case of error
#      raise exception(f"Error writing run to database: {str(e)}")

#    finally:
#      return
