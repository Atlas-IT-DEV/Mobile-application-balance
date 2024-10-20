-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Сен 08 2024 г., 16:54
-- Версия сервера: 5.7.39
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `Balance`
--

-- --------------------------------------------------------

--
-- Структура таблицы `companies`
--

CREATE TABLE IF NOT EXISTS `companies` (
  `id` int(11) NOT NULL,
  `name` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `contact` text COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `companies`
--

INSERT IGNORE INTO `companies` (`id`, `name`, `description`, `contact`) VALUES
(1, 'Tech Solutions', 'IT company', 'tech_solutions@example.com, +7-903-555-1234'),
(2, 'Green Energy', 'Eco energy', 'green_energy@example.com, +7-495-111-2222'),
(3, 'Food Express', 'Delivery', 'food_express@example.com, +7-905-777-3344'),
(4, 'Sky Media', 'Advertising', 'skymedia@example.com, +7-499-888-9900'),
(5, 'Health Co', 'Medical services', 'health_co@example.com, +7-926-123-4567');

-- --------------------------------------------------------

--
-- Структура таблицы `fees`
--

CREATE TABLE IF NOT EXISTS `fees` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `final_cost` decimal(10,2) NOT NULL,
  `gathered_cost` decimal(10,2) NOT NULL DEFAULT '0.00',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fee_category_id` int(11) NOT NULL,
  `image_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `fees`
--

INSERT IGNORE INTO `fees` (`id`, `name`, `description`, `final_cost`, `gathered_cost`, `created_at`, `fee_category_id`, `image_url`) VALUES
(1, 'Tech Conference', 'Annual tech conference 2024', '150000.00', '50000.00', '2024-09-08 14:00:00', 1, 'http://example.png'),
(2, 'Green Energy Forum', 'Sustainable energy event', '300000.00', '150000.00', '2024-09-08 14:15:00', 2, 'http://example.png'),
(3, 'Food Fair', 'Gourmet food exhibition', '100000.00', '60000.00', '2024-09-08 14:30:00', 3, 'http://example.png'),
(4, 'Media Summit', 'Media industry networking', '250000.00', '100000.00', '2024-09-08 14:45:00', 4, 'http://example.png'),
(5, 'Health Expo', 'Healthcare innovations', '500000.00', '200000.00', '2024-09-08 15:00:00', 5, 'http://example.png');

-- --------------------------------------------------------

--
-- Структура таблицы `fee_categories`
--

CREATE TABLE IF NOT EXISTS `fee_categories` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `fee_categories`
--

INSERT IGNORE INTO `fee_categories` (`id`, `name`) VALUES
(1, 'Healthcare'),
(2, 'Technology'),
(3, 'Sustainability'),
(4, 'Events'),
(5, 'Media & Advertising');

-- --------------------------------------------------------

--
-- Структура таблицы `history_payments`
--

CREATE TABLE IF NOT EXISTS `history_payments` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `fee_id` int(11) NOT NULL,
  `pay` decimal(10,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `history_payments`
--

INSERT IGNORE INTO `history_payments` (`id`, `user_id`, `fee_id`, `pay`, `created_at`) VALUES
(1, 1, 1, '10000.00', '2024-09-08 15:10:00'),
(2, 2, 2, '20000.00', '2024-09-08 15:20:00'),
(3, 3, 3, '5000.00', '2024-09-08 15:30:00'),
(4, 4, 4, '15000.00', '2024-09-08 15:40:00'),
(5, 5, 5, '25000.00', '2024-09-08 15:50:00');

-- --------------------------------------------------------

--
-- Структура таблицы `subscriptions`
--

CREATE TABLE IF NOT EXISTS `subscriptions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `fee_id` int(11) NOT NULL,
  `type_sub_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `subscriptions`
--

INSERT IGNORE INTO `subscriptions` (`id`, `user_id`, `fee_id`, `type_sub_id`) VALUES
(1, 1, 1, 1),
(2, 2, 2, 2),
(3, 3, 3, 1),
(4, 4, 4, 2),
(5, 5, 5, 1);

-- --------------------------------------------------------

--
-- Структура таблицы `sub_categories`
--

CREATE TABLE IF NOT EXISTS `sub_categories` (
  `id` int(11) NOT NULL,
  `type` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `sub_categories`
--

INSERT IGNORE INTO `sub_categories` (`id`, `type`) VALUES
(1, 'DAY'),
(2, 'MOUNTH');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL,
  `first_name` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `INN` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `data_register` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `role` enum('USER','ADMIN') COLLATE utf8mb4_unicode_ci DEFAULT 'USER'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `users`
--

-- Дамп данных таблицы `users` с красивыми и реалистичными значениями
INSERT IGNORE INTO `users` (`id`, `first_name`, `last_name`, `phone`, `INN`, `password`, `data_register`, `role`) VALUES
(1, 'John', 'Doe', '+7-903-123-4567', '7707083893', '$2y$10$Nm7B9uWsPgUm0UXDdy1S5uyp9/lnOqqrCkU7XMg9eGnb1G4EQWpXa', '2024-09-08 14:00:00', 'USER'),
(2, 'Jane', 'Smith', '+7-495-987-6543', '7705012397', '$2y$10$Nm7B9uWsPgUm0UXDdy1S5uyp9/lnOqqrCkU7XMg9eGnb1G4EQWpXa', '2024-09-08 14:05:00', 'ADMIN'),
(3, 'Alexander', 'Ivanov', '+7-905-334-2211', '7730023447', '$2y$10$Nm7B9uWsPgUm0UXDdy1S5uyp9/lnOqqrCkU7XMg9eGnb1G4EQWpXa', '2024-09-08 14:10:00', 'USER'),
(4, 'Maria', 'Petrova', '+7-499-443-3322', '7732124451', '$2y$10$Nm7B9uWsPgUm0UXDdy1S5uyp9/lnOqqrCkU7XMg9eGnb1G4EQWpXa', '2024-09-08 14:15:00', 'USER'),
(5, 'Oleg', 'Sidorov', '+7-926-556-6677', '7740015528', '$2y$10$4Em7G6pM9GjKEFfB9IxbhebTATLF6cx3dTjOjphLP9mFIZkdketYq', '2024-09-08 14:20:00', 'ADMIN');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `companies`
--
ALTER TABLE `companies`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `fees`
--
ALTER TABLE `fees`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fee_category_id` (`fee_category_id`);

--
-- Индексы таблицы `fee_categories`
--
ALTER TABLE `fee_categories`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `history_payments`
--
ALTER TABLE `history_payments`
  ADD PRIMARY KEY (`id`,`user_id`,`fee_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `fee_id` (`fee_id`);

--
-- Индексы таблицы `subscriptions`
--
ALTER TABLE `subscriptions`
  ADD PRIMARY KEY (`id`,`user_id`,`fee_id`,`type_sub_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `fee_id` (`fee_id`),
  ADD KEY `type_sub_id` (`type_sub_id`);

--
-- Индексы таблицы `sub_categories`
--
ALTER TABLE `sub_categories`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `companies`
--
ALTER TABLE `companies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT для таблицы `fees`
--
ALTER TABLE `fees`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT для таблицы `fee_categories`
--
ALTER TABLE `fee_categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT для таблицы `history_payments`
--
ALTER TABLE `history_payments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT для таблицы `subscriptions`
--
ALTER TABLE `subscriptions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `sub_categories`
--
ALTER TABLE `sub_categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=67;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `fees`
--
ALTER TABLE `fees`
  ADD CONSTRAINT `fees_ibfk_1` FOREIGN KEY (`fee_category_id`) REFERENCES `fee_categories` (`id`) ON DELETE CASCADE;

--
-- Ограничения внешнего ключа таблицы `history_payments`
--
ALTER TABLE `history_payments`
  ADD CONSTRAINT `history_payments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `history_payments_ibfk_2` FOREIGN KEY (`fee_id`) REFERENCES `fees` (`id`) ON DELETE CASCADE;

--
-- Ограничения внешнего ключа таблицы `subscriptions`
--
ALTER TABLE `subscriptions`
  ADD CONSTRAINT `subscriptions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `subscriptions_ibfk_2` FOREIGN KEY (`fee_id`) REFERENCES `fees` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `subscriptions_ibfk_3` FOREIGN KEY (`type_sub_id`) REFERENCES `sub_categories` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
