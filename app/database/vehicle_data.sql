-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 02 Feb 2025 pada 17.04
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `vehicle_db`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `vehicle_data`
--

CREATE TABLE `vehicle_data` (
  `id` int(11) NOT NULL,
  `vehicle_id` varchar(255) NOT NULL,
  `klasifikasikendaraan` varchar(50) DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  `time_crossed` datetime DEFAULT NULL,
  `drivingspeed` float DEFAULT NULL,
  `drivingdirection` varchar(10) DEFAULT NULL,
  `model_signature` varchar(100) DEFAULT NULL,
  `koordinat` varchar(255) NOT NULL,
  `warna` varchar(20) NOT NULL,
  `lokasisurvey` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `vehicle_data`
--

INSERT INTO `vehicle_data` (`id`, `vehicle_id`, `klasifikasikendaraan`, `timestamp`, `time_crossed`, `drivingspeed`, `drivingdirection`, `model_signature`, `koordinat`, `warna`, `lokasisurvey`) VALUES
(1, '2', 'motorcycle', '2025-02-02 22:03:06', NULL, 0, 'kanan', NULL, 'Atas', '', '1223'),
(2, '1', 'motorcycle', '2025-02-02 22:03:06', NULL, 0, 'kanan', NULL, 'Atas', '', '1223'),
(3, '3', 'truck', '2025-02-02 22:03:07', NULL, 0, 'kanan', NULL, 'Atas', '', '1223'),
(4, '2', 'motorcycle', '2025-02-02 22:18:53', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(5, '1', 'motorcycle', '2025-02-02 22:18:53', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(6, '3', 'truck', '2025-02-02 22:18:53', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(7, '15', 'car', '2025-02-02 22:18:57', NULL, 30, 'kanan', NULL, 'Atas', '', 'wew'),
(8, '20', 'truck', '2025-02-02 22:18:58', NULL, 11, 'kanan', NULL, 'Atas', '', 'wew'),
(9, '21', 'motorcycle', '2025-02-02 22:18:59', NULL, 70, 'kanan', NULL, 'Atas', '', 'wew'),
(10, '25', 'truck', '2025-02-02 22:18:59', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(11, '30', 'motorcycle', '2025-02-02 22:19:01', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(12, '28', 'motorcycle', '2025-02-02 22:19:01', NULL, 8, 'kanan', NULL, 'Atas', '', 'wew'),
(13, '29', 'car', '2025-02-02 22:19:01', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(14, '2', 'motorcycle', '2025-02-02 22:26:17', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(15, '1', 'motorcycle', '2025-02-02 22:26:17', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(16, '3', 'truck', '2025-02-02 22:26:18', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(17, '15', 'car', '2025-02-02 22:26:22', NULL, 26, 'kanan', NULL, 'Atas', '', 'wew'),
(18, '20', 'truck', '2025-02-02 22:26:23', NULL, 12, 'kanan', NULL, 'Atas', '', 'wew'),
(19, '21', 'motorcycle', '2025-02-02 22:26:24', NULL, 79, 'kanan', NULL, 'Atas', '', 'wew'),
(20, '25', 'truck', '2025-02-02 22:26:24', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(21, '2', 'motorcycle', '2025-02-02 22:29:13', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(22, '1', 'motorcycle', '2025-02-02 22:29:13', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(23, '3', 'truck', '2025-02-02 22:29:13', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(24, '2', 'motorcycle', '2025-02-02 22:29:41', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(25, '1', 'motorcycle', '2025-02-02 22:29:41', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(26, '3', 'truck', '2025-02-02 22:29:41', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(27, '15', 'car', '2025-02-02 22:29:45', NULL, 35, 'kanan', NULL, 'Atas', '', 'wew'),
(28, '20', 'truck', '2025-02-02 22:29:47', NULL, 12, 'kanan', NULL, 'Atas', '', 'wew'),
(29, '21', 'motorcycle', '2025-02-02 22:29:47', NULL, 48, 'kanan', NULL, 'Atas', '', 'wew'),
(30, '25', 'truck', '2025-02-02 22:29:48', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(31, '30', 'motorcycle', '2025-02-02 22:29:49', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(32, '28', 'motorcycle', '2025-02-02 22:29:49', NULL, 8, 'kanan', NULL, 'Atas', '', 'wew'),
(33, '29', 'car', '2025-02-02 22:29:49', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(34, '37', 'motorcycle', '2025-02-02 22:29:52', NULL, 22, 'kanan', NULL, 'Atas', '', 'wew'),
(35, '44', 'truck', '2025-02-02 22:29:53', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(36, '41', 'motorcycle', '2025-02-02 22:29:53', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(37, '47', 'truck', '2025-02-02 22:29:54', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(38, '46', 'truck', '2025-02-02 22:29:54', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(39, '45', 'truck', '2025-02-02 22:29:54', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(40, '50', 'motorcycle', '2025-02-02 22:29:54', NULL, 11, 'kanan', NULL, 'Atas', '', 'wew'),
(41, '49', 'car', '2025-02-02 22:29:57', NULL, 25, 'kanan', NULL, 'Atas', '', 'wew'),
(42, '62', 'car', '2025-02-02 22:29:57', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(43, '65', 'truck', '2025-02-02 22:30:00', NULL, 18, 'kanan', NULL, 'Atas', '', 'wew'),
(44, '74', 'truck', '2025-02-02 22:30:02', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(45, '67', 'truck', '2025-02-02 22:30:02', NULL, 24, 'kanan', NULL, 'Atas', '', 'wew'),
(46, '76', 'truck', '2025-02-02 22:30:03', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(47, '78', 'motorcycle', '2025-02-02 22:30:03', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(48, '77', 'motorcycle', '2025-02-02 22:30:03', NULL, 124, 'kanan', NULL, 'Atas', '', 'wew'),
(49, '81', 'motorcycle', '2025-02-02 22:30:04', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(50, '2', 'motorcycle', '2025-02-02 22:36:47', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(51, '1', 'motorcycle', '2025-02-02 22:36:47', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(52, '3', 'truck', '2025-02-02 22:36:48', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(53, '15', 'car', '2025-02-02 22:36:52', NULL, 41, 'kanan', NULL, 'Atas', '', 'wew'),
(54, '20', 'truck', '2025-02-02 22:36:53', NULL, 10, 'kanan', NULL, 'Atas', '', 'wew'),
(55, '21', 'motorcycle', '2025-02-02 22:36:53', NULL, 51, 'kanan', NULL, 'Atas', '', 'wew'),
(56, '25', 'truck', '2025-02-02 22:36:54', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(57, '30', 'motorcycle', '2025-02-02 22:36:55', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(58, '28', 'motorcycle', '2025-02-02 22:36:55', NULL, 8, 'kanan', NULL, 'Atas', '', 'wew'),
(59, '29', 'car', '2025-02-02 22:36:55', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(60, '37', 'motorcycle', '2025-02-02 22:36:59', NULL, 26, 'kanan', NULL, 'Atas', '', 'wew'),
(61, '44', 'truck', '2025-02-02 22:36:59', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(62, '41', 'motorcycle', '2025-02-02 22:36:59', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(63, '47', 'truck', '2025-02-02 22:37:00', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(64, '46', 'truck', '2025-02-02 22:37:00', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(65, '45', 'truck', '2025-02-02 22:37:00', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(66, '50', 'motorcycle', '2025-02-02 22:37:01', NULL, 12, 'kanan', NULL, 'Atas', '', 'wew'),
(67, '49', 'car', '2025-02-02 22:37:04', NULL, 27, 'kanan', NULL, 'Atas', '', 'wew'),
(68, '62', 'car', '2025-02-02 22:37:04', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(69, '65', 'truck', '2025-02-02 22:37:07', NULL, 15, 'kanan', NULL, 'Atas', '', 'wew'),
(70, '74', 'truck', '2025-02-02 22:37:09', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(71, '67', 'truck', '2025-02-02 22:37:09', NULL, 23, 'kanan', NULL, 'Atas', '', 'wew'),
(72, '76', 'truck', '2025-02-02 22:37:09', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(73, '78', 'motorcycle', '2025-02-02 22:37:10', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(74, '77', 'motorcycle', '2025-02-02 22:37:10', NULL, 108, 'kanan', NULL, 'Atas', '', 'wew'),
(75, '81', 'motorcycle', '2025-02-02 22:37:10', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(76, '83', 'truck', '2025-02-02 22:37:11', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(77, '82', 'truck', '2025-02-02 22:37:11', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(78, '2', 'motorcycle', '2025-02-02 22:41:07', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(79, '1', 'motorcycle', '2025-02-02 22:41:07', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(80, '3', 'truck', '2025-02-02 22:41:08', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(81, '15', 'car', '2025-02-02 22:41:12', NULL, 44, 'kanan', NULL, 'Atas', '', 'wew'),
(82, '20', 'truck', '2025-02-02 22:41:13', NULL, 14, 'kanan', NULL, 'Atas', '', 'wew'),
(83, '21', 'motorcycle', '2025-02-02 22:41:13', NULL, 76, 'kanan', NULL, 'Atas', '', 'wew'),
(84, '25', 'truck', '2025-02-02 22:41:14', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(85, '30', 'motorcycle', '2025-02-02 22:41:15', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(86, '28', 'motorcycle', '2025-02-02 22:41:15', NULL, 8, 'kanan', NULL, 'Atas', '', 'wew'),
(87, '29', 'car', '2025-02-02 22:41:15', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(88, '37', 'motorcycle', '2025-02-02 22:41:19', NULL, 22, 'kanan', NULL, 'Atas', '', 'wew'),
(89, '44', 'truck', '2025-02-02 22:41:19', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(90, '41', 'motorcycle', '2025-02-02 22:41:19', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(91, '47', 'truck', '2025-02-02 22:41:20', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(92, '46', 'truck', '2025-02-02 22:41:20', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(93, '45', 'truck', '2025-02-02 22:41:20', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(94, '50', 'motorcycle', '2025-02-02 22:41:21', NULL, 12, 'kanan', NULL, 'Atas', '', 'wew'),
(95, '49', 'car', '2025-02-02 22:41:24', NULL, 19, 'kanan', NULL, 'Atas', '', 'wew'),
(96, '62', 'car', '2025-02-02 22:41:24', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(97, '65', 'truck', '2025-02-02 22:41:27', NULL, 18, 'kanan', NULL, 'Atas', '', 'wew'),
(98, '74', 'truck', '2025-02-02 22:41:29', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(99, '67', 'truck', '2025-02-02 22:41:29', NULL, 34, 'kanan', NULL, 'Atas', '', 'wew'),
(100, '76', 'truck', '2025-02-02 22:41:29', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(101, '78', 'motorcycle', '2025-02-02 22:41:30', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(102, '77', 'motorcycle', '2025-02-02 22:41:30', NULL, 111, 'kanan', NULL, 'Atas', '', 'wew'),
(103, '81', 'motorcycle', '2025-02-02 22:41:30', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(104, '83', 'truck', '2025-02-02 22:41:31', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(105, '82', 'truck', '2025-02-02 22:41:31', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(106, '90', 'truck', '2025-02-02 22:41:31', NULL, 0, 'kanan', NULL, 'Atas', '', 'wew'),
(107, '93', 'car', '2025-02-02 22:41:33', NULL, 28, 'kanan', NULL, 'Atas', '', 'wew'),
(108, '94', 'truck', '2025-02-02 22:41:33', NULL, 7, 'kanan', NULL, 'Atas', '', 'wew'),
(109, '7', 'car', '2025-02-02 22:44:59', NULL, 29, 'kanan', NULL, 'Atas', '', '3434'),
(110, '9', 'car', '2025-02-02 22:45:00', NULL, 0, 'kanan', NULL, 'Atas', '', '3434'),
(111, '1', 'car', '2025-02-02 22:45:00', NULL, 41, 'kanan', NULL, 'Atas', '', '3434'),
(112, '11', 'bus', '2025-02-02 22:45:01', NULL, 24, 'kanan', NULL, 'Atas', '', '3434'),
(113, '20', 'bus', '2025-02-02 22:45:02', NULL, 0, 'kanan', NULL, 'Atas', '', '3434'),
(114, '5', 'car', '2025-02-02 22:45:02', NULL, 6, 'kanan', NULL, 'Atas', '', '3434'),
(115, '25', 'car', '2025-02-02 22:45:03', NULL, 0, 'kanan', NULL, 'Atas', '', '3434'),
(116, '10', 'car', '2025-02-02 22:45:04', NULL, 35, 'kanan', NULL, 'Atas', '', '3434'),
(117, '27', 'car', '2025-02-02 22:45:05', NULL, 26, 'kanan', NULL, 'Atas', '', '3434'),
(118, '31', 'truck', '2025-02-02 22:45:06', NULL, 22, 'kanan', NULL, 'Atas', '', '3434'),
(119, '29', 'car', '2025-02-02 22:45:07', NULL, 41, 'kanan', NULL, 'Atas', '', '3434'),
(120, '54', 'bus', '2025-02-02 22:45:08', NULL, 19, 'kanan', NULL, 'Atas', '', '3434'),
(121, '56', 'car', '2025-02-02 22:45:08', NULL, 16, 'kanan', NULL, 'Atas', '', '3434'),
(122, '40', 'car', '2025-02-02 22:45:08', NULL, 20, 'kanan', NULL, 'Atas', '', '3434'),
(123, '64', 'car', '2025-02-02 22:45:08', NULL, 0, 'kanan', NULL, 'Atas', '', '3434'),
(124, '73', 'bus', '2025-02-02 22:45:10', NULL, 6, 'kanan', NULL, 'Atas', '', '3434'),
(125, '53', 'bus', '2025-02-02 22:45:10', NULL, 22, 'kanan', NULL, 'Atas', '', '3434'),
(126, '78', 'car', '2025-02-02 22:45:10', NULL, 0, 'kanan', NULL, 'Atas', '', '3434'),
(127, '44', 'car', '2025-02-02 22:45:10', NULL, 37, 'kanan', NULL, 'Atas', '', '3434'),
(128, '55', 'car', '2025-02-02 22:45:11', NULL, 36, 'kanan', NULL, 'Atas', '', '3434'),
(129, '88', 'bus', '2025-02-02 22:45:11', NULL, 0, 'kanan', NULL, 'Atas', '', '3434'),
(130, '87', 'car', '2025-02-02 22:45:12', NULL, 19, 'kanan', NULL, 'Atas', '', '3434'),
(131, '63', 'car', '2025-02-02 22:45:12', NULL, 35, 'kanan', NULL, 'Atas', '', '3434'),
(132, '75', 'car', '2025-02-02 22:45:14', NULL, 48, 'kanan', NULL, 'Atas', '', '3434'),
(133, '104', 'car', '2025-02-02 22:45:17', NULL, 0, 'kanan', NULL, 'Atas', '', '3434'),
(134, '90', 'car', '2025-02-02 22:45:17', NULL, 22, 'kanan', NULL, 'Atas', '', '3434'),
(135, '109', 'bus', '2025-02-02 22:45:19', NULL, 25, 'kanan', NULL, 'Atas', '', '3434');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `vehicle_data`
--
  ALTER TABLE `vehicle_data`
    ADD PRIMARY KEY (`id`),
    ADD UNIQUE KEY `model_signature` (`model_signature`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `vehicle_data`
--
ALTER TABLE `vehicle_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=136;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
