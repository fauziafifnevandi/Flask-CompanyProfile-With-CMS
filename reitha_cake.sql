-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 25, 2021 at 07:25 PM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 7.4.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `reitha_cake`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

CREATE TABLE `accounts` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`id`, `username`, `password`, `email`) VALUES
(1, 'test', 'test', 'test@test.com'),
(2, 'fauzi', '123', 'fauzi@fauzi.com');

-- --------------------------------------------------------

--
-- Table structure for table `header`
--

CREATE TABLE `header` (
  `id` int(10) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `gambar` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `header`
--

INSERT INTO `header` (`id`, `nama`, `gambar`) VALUES
(1, 'ReithA Cake', 'loga.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `hubungi_kami`
--

CREATE TABLE `hubungi_kami` (
  `id` int(11) NOT NULL,
  `judul` varchar(100) NOT NULL,
  `isi` varchar(100) NOT NULL,
  `judul_informasi` varchar(100) NOT NULL,
  `nama_toko` varchar(100) NOT NULL,
  `alamat_toko` varchar(100) NOT NULL,
  `kota_toko` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `hubungi_kami`
--

INSERT INTO `hubungi_kami` (`id`, `judul`, `isi`, `judul_informasi`, `nama_toko`, `alamat_toko`, `kota_toko`) VALUES
(1, 'Kontak', 'Fitur layanan hubung untuk memberikan pesan dari para pelanggan kepada kami.', 'Informasi Kantor', 'ReithA Cake', 'Jl. Setia Budi Rahmawati No.12', 'Jakarta Pusat, Indonesia');

-- --------------------------------------------------------

--
-- Table structure for table `jumbotron`
--

CREATE TABLE `jumbotron` (
  `id` int(10) NOT NULL,
  `tagline` varchar(100) NOT NULL,
  `caption` varchar(100) NOT NULL,
  `gambar` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `jumbotron`
--

INSERT INTO `jumbotron` (`id`, `tagline`, `caption`, `gambar`) VALUES
(1, 'Rayakan Moment Terbaikmu Bersama RiethA Cake', 'Setiap Rasa Adalah Cerita.', 'jumbotron1.jpg'),
(2, 'Rayakan Moment Terbaikmu Bersama RiethA Cake', 'Setiap Rasa Adalah Cerita.', 'jumbotron2.jpg'),
(3, 'Rayakan Moment Terbaikmu Bersama RiethA Cake', 'Setiap Rasa Adalah Cerita.', 'jumbotron3.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `klien`
--

CREATE TABLE `klien` (
  `id` int(10) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `gambar` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `klien`
--

INSERT INTO `klien` (`id`, `nama`, `gambar`) VALUES
(1, 'gofood', 'klien1.png'),
(2, 'grabfood', 'klien2.png'),
(3, 'shopee', 'klien3.png');

-- --------------------------------------------------------

--
-- Table structure for table `paralax`
--

CREATE TABLE `paralax` (
  `id` int(10) NOT NULL,
  `gambar` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `paralax`
--

INSERT INTO `paralax` (`id`, `gambar`) VALUES
(1, 'paralax1.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `pelayanan`
--

CREATE TABLE `pelayanan` (
  `id` int(10) NOT NULL,
  `simbol` varchar(100) NOT NULL,
  `judul` varchar(100) NOT NULL,
  `isi` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `pelayanan`
--

INSERT INTO `pelayanan` (`id`, `simbol`, `judul`, `isi`) VALUES
(1, 'verified_user', 'Kualitas', ' Dengan menggunakan bahan berkualitas untuk menjaga kualitas produk '),
(2, 'work', 'Profesional', ' Berpengalaman dalam melayani berbagai macam produk bagi konsumen kami '),
(3, 'access_time', 'Kecepatan', ' Melayani dengan kecepatan yang sesuai dengan waktu pesanan untuk melayani anda semua ');

-- --------------------------------------------------------

--
-- Table structure for table `pesan`
--

CREATE TABLE `pesan` (
  `id` int(10) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `hp` varchar(100) NOT NULL,
  `pesan` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `pesan`
--

INSERT INTO `pesan` (`id`, `nama`, `email`, `hp`, `pesan`) VALUES
(1, 'Fauzi Afif Nevandi', 'fauzi@fauzi.com', '089123123123', 'Terimakasih atas pelayanan ReithA Cake yang memuaskan!'),
(2, 'Rahmat Darmawan', 'rahmat@rahmat.com', '081123123123', 'Saya suka dengan pelayanan dan produk yang diberikan!'),
(3, 'Kevin Sanjaya', 'kevin@kevin.com', '081543123123', 'Rotinya enak dan lembut, sangat cocok dimakan setelah pertandingan maupun saat latihan, maju terus R'),
(4, 'Purnomo Ojek RCTI', 'purnomo@purnomo.com', '081567123123', 'Saya purnomo dan menikmati rasa roti maupun produk dari ReithA Cake! Terimakasih atas pencapaianya!'),
(5, 'Agus Rahmat', 'agus@agus.com', '087123123123', 'Saya tidak merasa salah memilih ReithA Cake untuk hidangan resepsi nikahan saya, maju terus!'),
(6, 'Steven Darmawan', 'steven@steven.com', '081543123', 'Roti yang enak, saya suka!'),
(7, 'Fahum Darmawan', 'fahum@faum.com', '085123123123', 'Cocok sekali untuk dihidangkan bersama keluarga besar, saya suka ReithA Cake!');

-- --------------------------------------------------------

--
-- Table structure for table `produk`
--

CREATE TABLE `produk` (
  `id` int(10) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `gambar` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `produk`
--

INSERT INTO `produk` (`id`, `nama`, `gambar`) VALUES
(1, 'kue1', 'produk1.jpg'),
(2, 'kue2', 'produk2.jpg'),
(3, 'qwe', 'produk3.jpg'),
(4, 'fdgd', 'produk4.jpg'),
(5, 'rdggd', 'produk5.jpg'),
(6, 'drgdrg', 'produk6.jpg'),
(7, 'rgdrgd', 'produk7.jpg'),
(8, 'rgdrg', 'produk8.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `tentang`
--

CREATE TABLE `tentang` (
  `id` int(10) NOT NULL,
  `judul` varchar(100) NOT NULL,
  `isi` text NOT NULL,
  `moto1` varchar(100) NOT NULL,
  `moto2` varchar(100) NOT NULL,
  `moto3` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tentang`
--

INSERT INTO `tentang` (`id`, `judul`, `isi`, `moto1`, `moto2`, `moto3`) VALUES
(1, 'Percayakan Pada Profesional', ' Perusahaan kami merupakan profesional yang bergerak pada kuliner roti dengan kualitas terbaik. Dengan melayani berbagai macam aneka roti baik sebagai hadiah maupun konsumsi kami siap memberikan yang terbaik untuk anda. ', 'KUALITAS', 'PROFESIONAL', 'KECEPATAN');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `header`
--
ALTER TABLE `header`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `hubungi_kami`
--
ALTER TABLE `hubungi_kami`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `jumbotron`
--
ALTER TABLE `jumbotron`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `klien`
--
ALTER TABLE `klien`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `paralax`
--
ALTER TABLE `paralax`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pelayanan`
--
ALTER TABLE `pelayanan`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pesan`
--
ALTER TABLE `pesan`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `produk`
--
ALTER TABLE `produk`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tentang`
--
ALTER TABLE `tentang`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts`
--
ALTER TABLE `accounts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `header`
--
ALTER TABLE `header`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `hubungi_kami`
--
ALTER TABLE `hubungi_kami`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `jumbotron`
--
ALTER TABLE `jumbotron`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `klien`
--
ALTER TABLE `klien`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `paralax`
--
ALTER TABLE `paralax`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `pelayanan`
--
ALTER TABLE `pelayanan`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `pesan`
--
ALTER TABLE `pesan`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `produk`
--
ALTER TABLE `produk`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `tentang`
--
ALTER TABLE `tentang`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
