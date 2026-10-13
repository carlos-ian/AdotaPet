-- 6.4 FULL OUTER JOIN: adoções x apadrinhamentos pelo par (adotante, animal)
SELECT COALESCE(ad.id_adotante, ap.id_adotante) AS id_adotante,
       COALESCE(ad.id_animal,   ap.id_animal)   AS id_animal,
       ad.status AS status_adocao, ap.status AS status_apadrinhamento,
       CASE
           WHEN ad.id_animal IS NOT NULL AND ap.id_animal IS NOT NULL THEN 'Adoção e apadrinhamento'
           WHEN ad.id_animal IS NOT NULL THEN 'Somente adoção'
           ELSE 'Somente apadrinhamento'
       END AS tipo_relacao
FROM adota ad
FULL OUTER JOIN apadrinha ap
       ON ap.id_adotante = ad.id_adotante AND ap.id_animal = ad.id_animal;
