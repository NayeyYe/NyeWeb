-- 创建数据库
CREATE DATABASE IF NOT EXISTS `nyeweb` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE `nyeweb`;

-- 文章表
CREATE TABLE IF NOT EXISTS `articles`
(
    `id`       INT AUTO_INCREMENT PRIMARY KEY,
    `title`    VARCHAR(255) NOT NULL,
    `slug`     VARCHAR(255) NOT NULL UNIQUE,
    `category` VARCHAR(100),
    `date`     DATE,
    `summary`  TEXT,
    `status`   TINYINT NOT NULL DEFAULT 1 COMMENT '0=未发布, 1=已发布, 2=已回收'
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

-- 项目表
CREATE TABLE IF NOT EXISTS `projects`
(
    `id`      INT AUTO_INCREMENT PRIMARY KEY,
    `title`   VARCHAR(255) NOT NULL,
    `slug`    VARCHAR(255) NOT NULL UNIQUE,
    `date`    DATE,
    `summary` TEXT,
    `status`  TINYINT NOT NULL DEFAULT 1 COMMENT '0=未发布, 1=已发布, 2=已回收'
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

-- 书籍表
CREATE TABLE IF NOT EXISTS `books`
(
    `id`          INT AUTO_INCREMENT PRIMARY KEY,
    `title`       VARCHAR(255) NOT NULL,
    `description` TEXT,
    `filename`    VARCHAR(255),
    `cover`       VARCHAR(255),
    `status`  TINYINT NOT NULL DEFAULT 1 COMMENT '0=未发布, 1=已发布, 2=已回收'
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

-- 图表示
CREATE TABLE IF NOT EXISTS `figures`
(
    `id`          INT AUTO_INCREMENT PRIMARY KEY,
    `title`       VARCHAR(255) NOT NULL,
    `description` TEXT,
    `filename`    VARCHAR(255),
    `status`      TINYINT NOT NULL DEFAULT 1 COMMENT '0=未发布, 1=已发布, 2=已回收'
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

-- 工具表
CREATE TABLE IF NOT EXISTS `tools`
(
    `id`          INT AUTO_INCREMENT PRIMARY KEY,
    `title`       VARCHAR(255) NOT NULL,
    `description` TEXT,
    `url`         VARCHAR(2083),
    `status`      TINYINT NOT NULL DEFAULT 1 COMMENT '0=未发布, 1=已发布, 2=已回收'
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

-- 标签表 (通用)
CREATE TABLE IF NOT EXISTS `tags`
(
    `id`   INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL UNIQUE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

-- 文章与标签的关联表
CREATE TABLE IF NOT EXISTS `article_tags`
(
    `article_id` INT,
    `tag_id`     INT,
    PRIMARY KEY (`article_id`, `tag_id`),
    FOREIGN KEY (`article_id`) REFERENCES `articles` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

-- 项目与标签的关联表
CREATE TABLE IF NOT EXISTS `project_tags`
(
    `project_id` INT,
    `tag_id`     INT,
    PRIMARY KEY (`project_id`, `tag_id`),
    FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

-- 书籍与标签的关联表
CREATE TABLE IF NOT EXISTS `book_tags`
(
    `book_id` INT,
    `tag_id`  INT,
    PRIMARY KEY (`book_id`, `tag_id`),
    FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

-- 图表与标签的关联表
CREATE TABLE IF NOT EXISTS `figure_tags`
(
    `figure_id` INT,
    `tag_id`    INT,
    PRIMARY KEY (`figure_id`, `tag_id`),
    FOREIGN KEY (`figure_id`) REFERENCES `figures` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

-- 工具与标签的关联表
CREATE TABLE IF NOT EXISTS `tool_tags`
(
    `tool_id` INT,
    `tag_id`  INT,
    PRIMARY KEY (`tool_id`, `tag_id`),
    FOREIGN KEY (`tool_id`) REFERENCES `tools` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

-- 时间线表
CREATE TABLE IF NOT EXISTS `timeline`
(
    `id`        INT AUTO_INCREMENT PRIMARY KEY,
    `timestamp` DATETIME NOT NULL,
    `content`   TEXT     NOT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

-- 收藏图片表
CREATE TABLE IF NOT EXISTS `favorite_images`
(
    `id`       INT AUTO_INCREMENT PRIMARY KEY,
    `filename` VARCHAR(255) NOT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

