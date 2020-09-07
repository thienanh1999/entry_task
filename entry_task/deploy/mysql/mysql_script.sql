USE entry_task_db;

CREATE TABLE `user_tab` (
  `id` int unsigned PRIMARY KEY AUTO_INCREMENT,
  `username` varchar(255),
  `fullname` varchar(255),
  `hashed_password` varchar(255),
  `salt` varchar(255),
  `verify_code` varchar(255),
  `created_at` int unsigned,
  `is_admin` int unsigned
);
CREATE UNIQUE INDEX `idx_username` ON `user_tab` (`username`);

CREATE TABLE `event_tab` (
  `id` int unsigned PRIMARY KEY AUTO_INCREMENT,
  `title` varchar(255),
  `description` varchar(255),
  `created_at` int unsigned,
  `start` int unsigned,
  `end` int unsigned,
  `location` varchar(255),
  `images` varchar(1000)
);
CREATE INDEX `idx_location` ON `event_tab` (`location`);
CREATE INDEX `idx_end_start` ON `event_tab` (`end`, `start`);
CREATE INDEX `idx_title_location` ON `event_tab` (`title`, `location`);

CREATE TABLE `like_tab` (
  `id` int unsigned PRIMARY KEY AUTO_INCREMENT,
  `user_id` int unsigned,
  `event_id` int unsigned,
  `is_deleted` int unsigned
);
CREATE UNIQUE INDEX `idx_event_id_user_id` ON `like_tab` (`event_id`, `user_id`);
CREATE UNIQUE INDEX `idx_user_id_event_id` ON `like_tab` (`user_id`, `event_id`);

CREATE TABLE `comment_tab` (
  `id` int unsigned PRIMARY KEY AUTO_INCREMENT,
  `user_id` int unsigned,
  `event_id` int unsigned,
  `comment` text,
  `created_at` int unsigned
);
CREATE INDEX `idx_event_id` ON `comment_tab` (`event_id`);

CREATE TABLE `paticipant_tab` (
  `id` int unsigned PRIMARY KEY AUTO_INCREMENT,
  `user_id` int unsigned,
  `event_id` int unsigned,
  `is_deleted` int unsigned
);
CREATE UNIQUE INDEX `idx_event_id_user_id` ON `paticipant_tab` (`event_id`, `user_id`);
CREATE UNIQUE INDEX `idx_user_id_event_id` ON `paticipant_tab` (`user_id`, `event_id`);

CREATE TABLE `category_tab` (
  `id` int unsigned PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255)
);

CREATE TABLE `event_category_tab` (
  `id` int unsigned PRIMARY KEY AUTO_INCREMENT,
  `event_id` int unsigned,
  `category_id` int unsigned
);
CREATE UNIQUE INDEX `idx_category_id_event_id` ON `event_category_tab` (`category_id`, `event_id`);
CREATE INDEX `idx_event_id` ON `event_category_tab` (`event_id`);
