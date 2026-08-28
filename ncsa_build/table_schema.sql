CREATE TABLE IF NOT EXISTS `xalt_link` (
  `link_id`          int(11)   unsigned NOT NULL auto_increment,

  `uuid`             char(36)           NOT NULL,
  `hash_id`          char(40)           NOT NULL,
  `date`             DATETIME           NOT NULL,

  `link_program`     varchar(64)        NOT NULL,
  `link_path`        varchar(1024)      NOT NULL,
  `link_module_name` varchar(64)                ,

  `link_line`        blob                       ,
  `cwd`              varchar(1024)              ,
  `build_user`       varchar(64)        NOT NULL,

  `build_syshost`    varchar(64)        NOT NULL,
  `build_epoch`      double             NOT NULL,
  `exec_path`        varchar(1024)      NOT NULL,

  PRIMARY KEY  (`link_id`),
  INDEX  `index_date` (`date`),
  UNIQUE  KEY  `uuid` (`uuid`)
) DEFAULT CHARSET=utf8  COLLATE=utf8_bin AUTO_INCREMENT=1


CREATE TABLE IF NOT EXISTS `xalt_object` (
  `obj_id`        int(11)   unsigned NOT NULL auto_increment,
  `object_path`   varchar(1024)      NOT NULL,
  `syshost`       varchar(64)        NOT NULL,
  `hash_id`       char(40)           NOT NULL,
  `module_name`   varchar(64)                ,  
  `timestamp`     TIMESTAMP                  ,
  `lib_type`      char(2)            NOT NULL,
  PRIMARY KEY  (`obj_id`),
  INDEX  `index_hash_id` (`hash_id`),
  INDEX  `thekey` (`object_path`(128), `hash_id`, `syshost`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8  COLLATE=utf8_bin AUTO_INCREMENT=1




CREATE TABLE IF NOT EXISTS `xalt_run` (
  `run_id`        int(11)     unsigned NOT NULL auto_increment,
  `job_id`        char(64)             NOT NULL,
  `run_uuid`      char(36)             NOT NULL,
  `date`          datetime             NOT NULL,
  `start_end`     char(3)              NOT NULL,

  `syshost`       varchar(64)          NOT NULL,
  `uuid`          char(36)                     ,
  `hash_id`       char(40)             NOT NULL,

  `account`       varchar(20)          NOT NULL,
  `exec_type`     char(7)              NOT NULL,
  `start_time`    double               NOT NULL,

  `end_time`      double               NOT NULL,
  `run_time`      double               NOT NULL,
  `probability`   double               NOT NULL,
  `num_cores`     int(11)     unsigned NOT NULL,

  `num_nodes`     int(11)     unsigned NOT NULL,
  `num_threads`   smallint(6) unsigned NOT NULL,
  `num_gpus`      int(11)     unsigned NOT NULL,

  `queue`         varchar(64)          NOT NULL,
  `sum_runs`      int(11)     unsigned NOT NULL,
  `sum_time`      double               NOT NULL,

  `user`          varchar(32)          NOT NULL,
  `exec_path`     varchar(1024)        NOT NULL,
  `module_name`   varchar(64)                  ,
  `cwd`           varchar(1024)        NOT NULL,
  `cmdline`       blob                 NOT NULL,
  `container`     varchar(32)                  ,
  PRIMARY KEY             (`run_id`   ),
  INDEX  `index_date`     (`date`     ),
  INDEX  `index_run_uuid` (`run_uuid` ),
  INDEX `thekey` (`job_id`, `syshost` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1




CREATE TABLE IF NOT EXISTS `join_run_object` (
  `join_id`       int(11)      unsigned  NOT NULL auto_increment,
  `obj_id`        int(11)      unsigned  NOT NULL,
  `run_id`        int(11)      unsigned  NOT NULL,
  `date`          DATE                   NOT NULL,

  PRIMARY KEY (`join_id`),
  FOREIGN KEY (`run_id`)  REFERENCES `xalt_run`(`run_id`),
  FOREIGN KEY (`obj_id`)  REFERENCES `xalt_object`(`obj_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8  COLLATE=utf8_bin AUTO_INCREMENT=1


CREATE TABLE IF NOT EXISTS `xalt_env_name` (
  `env_id`        int(20) unsigned  NOT NULL auto_increment,
  `env_name`      varchar(64)       NOT NULL,
  PRIMARY KEY  (`env_id`),
  UNIQUE  KEY  `env_name` (`env_name`),
  INDEX        `a_env_name` (`env_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8  COLLATE=utf8_bin AUTO_INCREMENT=1




CREATE TABLE IF NOT EXISTS `join_run_env` (
  `join_id`       bigint(20) unsigned   NOT NULL auto_increment,
  `env_id`        int(11)    unsigned   NOT NULL,
  `run_id`        int(11)    unsigned   NOT NULL,
  `date`          DATE                  NOT NULL,
  `env_value`     blob                  NOT NULL,
  PRIMARY KEY (`join_id`),
  FOREIGN KEY (`env_id`)  REFERENCES `xalt_env_name`(`env_id`),
  FOREIGN KEY (`run_id`)  REFERENCES `xalt_run`(`run_id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8  COLLATE=utf8_bin AUTO_INCREMENT=1



CREATE TABLE IF NOT EXISTS `xalt_user` (
  `usr_id`        int(11)     unsigned NOT NULL auto_increment,
  `user`          varchar(32)          NOT NULL,
  `anon_user`     varchar(12)          NOT NULL,
  PRIMARY KEY (`usr_id`),
  INDEX `the_user` (`user`),
  INDEX `a_user`   (`anon_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8  COLLATE=utf8_bin AUTO_INCREMENT=1



CREATE TABLE IF NOT EXISTS `xalt_account` (
  `acct_id`          int(11)      unsigned NOT NULL auto_increment,
  `account`          varchar(32)           NOT NULL,
  `anon_user`        varchar(10)           NOT NULL,
  `field_of_science` varchar(64)           NOT NULL,
  PRIMARY KEY (`acct_id`),
  INDEX `the_account` (`account`),
  INDEX `a_acct`   (`anon_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8  COLLATE=utf8_bin AUTO_INCREMENT=1



CREATE TABLE IF NOT EXISTS `xalt_function` (
  `func_id`       int(11)        unsigned NOT NULL auto_increment,
  `function_name` varchar(255)            NOT NULL,
  PRIMARY KEY  (`func_id`),
  UNIQUE  KEY  `function_name` (`function_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8  COLLATE=utf8_bin AUTO_INCREMENT=1



CREATE TABLE IF NOT EXISTS `join_link_function` (
  `join_id`       int(11)       unsigned NOT NULL auto_increment,
  `func_id`       int(11)       unsigned NOT NULL,
  `link_id`       int(11)       unsigned NOT NULL,
  `date`          DATE                   NOT NULL,
  PRIMARY KEY (`join_id`),
  FOREIGN KEY (`func_id`)  REFERENCES `xalt_function`(`func_id`),
  FOREIGN KEY (`link_id`)  REFERENCES `xalt_link`(`link_id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8  COLLATE=utf8_bin AUTO_INCREMENT=1


CREATE TABLE IF NOT EXISTS `xalt_total_env` (
  `envT_id`       bigint(20) unsigned NOT NULL auto_increment,
  `run_id`        int(11)    unsigned NOT NULL,
  `date`          DATE                NOT NULL,
  `env_blob`      blob                NOT NULL,
  PRIMARY KEY (`envT_id`),
  FOREIGN KEY (`run_id`)  REFERENCES `xalt_run`(`run_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8  COLLATE=utf8_bin AUTO_INCREMENT=1


  ALTER TABLE `join_link_function` 
  ADD UNIQUE `unique_func_link_id` ( `func_id`, `link_id` )


CREATE TABLE IF NOT EXISTS `xalt_pkg` (
  `pkg_id`        bigint(20)     unsigned NOT NULL auto_increment,
  `run_id`        int(11)        unsigned NOT NULL,
  `run_uuid`      char(36)             NOT NULL,
  `program`       varchar(12)             NOT NULL,
  `pkg_name`      varchar(64)             NOT NULL,
  `pkg_version`   varchar(32)                     ,
  `pkg_path`      varchar(1024)                   ,
  PRIMARY KEY (`pkg_id`),
  FOREIGN KEY (`run_uuid`)  REFERENCES `xalt_run`(`run_uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8  COLLATE=utf8_bin AUTO_INCREMENT=1




