SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS schedules (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    start_datetime DATETIME NOT NULL,
    end_datetime DATETIME,
    completed BOOLEAN DEFAULT FALSE, -- 'is_completed'에서 'completed'로 수정
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- INSERT 쿼리도 'completed'로 수정
INSERT INTO `schedule_db`.`schedules` (`title`, `description`, `start_datetime`, `end_datetime`, `completed`) VALUES ("풋살", "정기 풋살 모임", '20251015080000', '20251015090000', '1');`start_datetime`, `end_datetime`, `is_completed`) VALUES ("풋살", "정기 풋살 모임", '20251015080000', '20251015090000', '1');