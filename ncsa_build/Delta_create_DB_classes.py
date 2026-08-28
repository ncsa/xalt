from typing import List, Dict, Tuple
from datetime import datetime



class PkgObj():
#  def __init__(self, data, path):
  def __init__(self, data):
#      self.path = path
      self.xalt_run_uuid = data.get('xalt_run_uuid')
      self.pkg_version = data.get('pkg_version')
      self.pkg_name = data.get('pkg_name')
      self.pkg_path = data.get('pkg_path')
  def writeToDB(self, conn):
    """
    Write new package data to the database using provided MariaDB connection.
    Uses xalt_run_uuid directly as run_id and 'python' as program.
    
    Args:
        conn: MariaDB connection object
    
    Returns:
        pkg_id: The ID of the inserted package record
    """
    cursor = conn.cursor()
    try:



cursor.execute("""
        CREATE TABLE IF NOT EXISTS `xalt_pkg` (
          `pkg_id`        bigint(20)     unsigned NOT NULL auto_increment,
          `run_id`        int(11)        unsigned NOT NULL,
          `program`       varchar(12)             NOT NULL,
          `pkg_name`      varchar(64)             NOT NULL,
          `pkg_version`   varchar(32)                     ,
          `pkg_path`      varchar(1024)                   ,
          PRIMARY KEY (`pkg_id`),
          FOREIGN KEY (`run_id`)  REFERENCES `xalt_run`(`run_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8  COLLATE=utf8_bin AUTO_INCREMENT=1
        """)
    print("(%d) create xalt_pkg table" % idx); idx += 1


            pkg_id = cursor.lastrowid
        conn.commit()
        
        return pkg_id
        
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error writing package to database: {str(e)}")
    finally:
        cursor.close()
     
