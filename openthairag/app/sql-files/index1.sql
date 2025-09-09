CREATE TABLE `health_products` (
  `id` INT AUTO_INCREMENT,
  `Type` VARCHAR(255) COMMENT 'ประเภทสินค้า เช่น ยา หรืออาหารเสริม',
  `ProductName` VARCHAR(255) COMMENT 'ชื่อสินค้า',
  `Price` VARCHAR(255) COMMENT 'ราคาพร้อมหน่วย เช่น บาท/ปริมาณ',
  `Description` TEXT COMMENT 'รายละเอียดสินค้า',
  `HowtoUse` TEXT COMMENT 'วิธีใช้สินค้า',
  `Caution` TEXT COMMENT 'ข้อควรระวัง',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;