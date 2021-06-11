CREATE SCHEMA IF NOT EXISTS practica_aos;
USE practica_aos;
CREATE TABLE vehiculos(id INT AUTO_INCREMENT,clienteId INT NOT NULL,
			matricula VARCHAR(10) NOT NULL,marca VARCHAR(20) NOT NULL ,
			modelo VARCHAR(50) NOT NULL,color VARCHAR(20) NOT NULL,
			anio INT NOT NULL, VIN VARCHAR(50) NOT NULL,PRIMARY KEY(id)) ;

INSERT INTO `vehiculos` (`id`, `clienteId`, `matricula`, `marca`, `modelo`, `color`, `anio`, `VIN`) VALUES
					    (1, 5, '7324-DBH', 'Ford', 'Focus', 'Negro', 2017, '1B3BG26P3FX513068'),
					    (2, 22, '2420-RPT', 'Audi', 'a6', 'Azul', 2015, 'JH4KA3161HC006800'),
					    (3, 32, '8472-ANJ', 'KIA', 'Sportage', 'Blanco', 2021, '1G8ZF52801Z328015'),
					    (4, 32, '7482-CJD', 'BMW', '328i', 'Negro', 2012, 'JH4DA9460NS007560');


ALTER TABLE `vehiculos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;
