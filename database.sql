-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema poodle_learn
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema poodle_learn
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `poodle_learn` DEFAULT CHARACTER SET utf8mb4 ;
USE `poodle_learn` ;

-- -----------------------------------------------------
-- Table `poodle_learn`.`teachers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `poodle_learn`.`teachers` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(200) NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `poodle_learn`.`courses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `poodle_learn`.`courses` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `owner_id` INT(11) NOT NULL,
  `title` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NOT NULL,
  `objectives` VARCHAR(45) NOT NULL,
  `private` TINYINT(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `title_UNIQUE` (`title` ASC) VISIBLE,
  INDEX `fk_Courses_Teachers_idx` (`owner_id` ASC) VISIBLE,
  CONSTRAINT `fk_Courses_Teachers`
    FOREIGN KEY (`owner_id`)
    REFERENCES `poodle_learn`.`teachers` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 16
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `poodle_learn`.`tags`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `poodle_learn`.`tags` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `tag` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 12
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `poodle_learn`.`course_has_tags`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `poodle_learn`.`course_has_tags` (
  `course_id` INT(11) NOT NULL,
  `tag_id` INT(11) NOT NULL,
  PRIMARY KEY (`course_id`, `tag_id`),
  INDEX `fk_courses_has_tags_tags1_idx` (`tag_id` ASC) VISIBLE,
  INDEX `fk_courses_has_tags_courses1_idx` (`course_id` ASC) VISIBLE,
  CONSTRAINT `fk_courses_has_tags_courses1`
    FOREIGN KEY (`course_id`)
    REFERENCES `poodle_learn`.`courses` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_courses_has_tags_tags1`
    FOREIGN KEY (`tag_id`)
    REFERENCES `poodle_learn`.`tags` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `poodle_learn`.`sections`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `poodle_learn`.`sections` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `course_id` INT(11) NOT NULL,
  `title` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NULL DEFAULT NULL,
  `content` VARCHAR(500) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Sections_Courses1_idx` (`course_id` ASC) VISIBLE,
  CONSTRAINT `fk_Sections_Courses1`
    FOREIGN KEY (`course_id`)
    REFERENCES `poodle_learn`.`courses` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `poodle_learn`.`students`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `poodle_learn`.`students` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(200) NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 19
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `poodle_learn`.`student_has_subscriptions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `poodle_learn`.`student_has_subscriptions` (
  `student_id` INT(11) NOT NULL,
  `course_id` INT(11) NOT NULL,
  PRIMARY KEY (`student_id`, `course_id`),
  INDEX `fk_Students_has_Courses_Courses1_idx` (`course_id` ASC) VISIBLE,
  INDEX `fk_Students_has_Courses_Students1_idx` (`student_id` ASC) VISIBLE,
  CONSTRAINT `fk_Students_has_Courses_Courses1`
    FOREIGN KEY (`course_id`)
    REFERENCES `poodle_learn`.`courses` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Students_has_Courses_Students1`
    FOREIGN KEY (`student_id`)
    REFERENCES `poodle_learn`.`students` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
