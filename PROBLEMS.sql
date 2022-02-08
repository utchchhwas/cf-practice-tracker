/*
 Navicat Premium Data Transfer

 Source Server         : CF
 Source Server Type    : Oracle
 Source Server Version : 190000
 Source Schema         : C##CF

 Target Server Type    : Oracle
 Target Server Version : 190000
 File Encoding         : 65001

 Date: 09/02/2022 01:41:45
*/


-- ----------------------------
-- Table structure for PROBLEMS
-- ----------------------------
DROP TABLE "C##CF"."PROBLEMS";
CREATE TABLE "C##CF"."PROBLEMS" (
  "index" VARCHAR2(10 BYTE) VISIBLE NOT NULL,
  "contest_id" NUMBER VISIBLE NOT NULL,
  "problem_name" VARCHAR2(255 BYTE) VISIBLE NOT NULL,
  "rating" NUMBER VISIBLE NOT NULL
);

-- ----------------------------
-- Records of PROBLEMS
-- ----------------------------
INSERT INTO "C##CF"."PROBLEMS" VALUES ('A', '1621', 'Stable Arrangement of Rooks', '800');
INSERT INTO "C##CF"."PROBLEMS" VALUES ('B', '1621', 'Integers Shop', '1500');
INSERT INTO "C##CF"."PROBLEMS" VALUES ('C', '1621', 'Hidden Permutations', '1700');
INSERT INTO "C##CF"."PROBLEMS" VALUES ('D', '1621', 'The Winter Hike', '2100');
INSERT INTO "C##CF"."PROBLEMS" VALUES ('E', '1621', 'New School', '2300');
INSERT INTO "C##CF"."PROBLEMS" VALUES ('A', '1624', 'Plus One on the Subset', '800');
INSERT INTO "C##CF"."PROBLEMS" VALUES ('B', '1624', 'Make AP', '900');
INSERT INTO "C##CF"."PROBLEMS" VALUES ('C', '1624', 'Division by Two and Permutation', '1100');
INSERT INTO "C##CF"."PROBLEMS" VALUES ('D', '1624', 'Palindromes Coloring', '1400');

-- ----------------------------
-- Primary Key structure for table PROBLEMS
-- ----------------------------
ALTER TABLE "C##CF"."PROBLEMS" ADD CONSTRAINT "SYS_C007811" PRIMARY KEY ("contest_id", "index");
