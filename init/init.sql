-- Create database if it doesn't exist
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;


CREATE DATABASE IF NOT EXISTS customer_service_db
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

-- Switch to this database
USE customer_service_db;

-- Create table
CREATE TABLE IF NOT EXISTS `health_products` (
  `id` INT AUTO_INCREMENT,
  `Type` VARCHAR(255) COMMENT 'ประเภทสินค้า เช่น ยา หรืออาหารเสริม',
  `ProductName` VARCHAR(255) COMMENT 'ชื่อสินค้า',
  `Price` VARCHAR(255) COMMENT 'ราคาพร้อมหน่วย เช่น บาท/ปริมาณ',
  `Description` TEXT COMMENT 'รายละเอียดสินค้า',
  `HowtoUse` TEXT COMMENT 'วิธีใช้สินค้า',
  `Caution` TEXT COMMENT 'ข้อควรระวัง',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert mock data
INSERT INTO `health_products` 
(`Type`, `ProductName`, `Price`, `Description`, `HowtoUse`, `Caution`) VALUES
('ยา', 'Paracetamol 500mg', '35 บาท/แผง (10 เม็ด)', 'ยาลดไข้ บรรเทาอาการปวดศีรษะ ปวดเมื่อย', 'รับประทานครั้งละ 1-2 เม็ด ทุก 4-6 ชั่วโมง เมื่อมีอาการ', 'ห้ามรับประทานเกินวันละ 8 เม็ด และควรระวังผู้ป่วยโรคตับ'),
('อาหารเสริม', 'Vitamin C 1000mg', '250 บาท/ขวด (30 เม็ด)', 'เสริมภูมิคุ้มกันและช่วยในการดูดซึมธาตุเหล็ก', 'รับประทานครั้งละ 1 เม็ด วันละ 1 ครั้ง พร้อมอาหาร', 'ควรระวังการรับประทานเกินปริมาณ อาจทำให้เกิดนิ่วในไต'),
('อาหารเสริม', 'Fish Oil Omega-3', '450 บาท/ขวด (60 เม็ด)', 'ช่วยบำรุงสมองและหัวใจ ลดไขมันในเลือด', 'รับประทานครั้งละ 1 เม็ด วันละ 2 ครั้ง หลังอาหาร', 'ควรระวังในผู้ที่ทานยาละลายลิ่มเลือด'),
('ยา', 'Cetirizine 10mg', '60 บาท/แผง (10 เม็ด)', 'ยาต้านฮีสตามีน บรรเทาอาการแพ้ คัน ลมพิษ', 'รับประทานครั้งละ 1 เม็ด วันละครั้ง ก่อนนอน', 'อาจทำให้ง่วงซึม ไม่ควรขับรถหรือทำงานกับเครื่องจักร'),
('อาหารเสริม', 'Calcium-D', '300 บาท/ขวด (60 เม็ด)', 'บำรุงกระดูกและฟัน เสริมวิตามินดี', 'รับประทานครั้งละ 1 เม็ด วันละ 1-2 ครั้ง พร้อมอาหาร', 'ควรระวังในผู้ป่วยโรคไตหรือนิ่วในทางเดินปัสสาวะ');
