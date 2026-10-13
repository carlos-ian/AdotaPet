-- 9.2 Padrinhos com contribuição ativa equivalente mensal acima de R$ 100
SELECT ado.nome AS padrinho,
       COUNT(*) AS qtd_afilhados,
       ROUND(SUM(CASE ap.frequencia
                     WHEN 'Trimestral' THEN ap.valor_recorrente / 3
                     WHEN 'Anual'      THEN ap.valor_recorrente / 12
                     ELSE ap.valor_recorrente
                 END), 2) AS contribuicao_mensal
FROM apadrinha ap
JOIN adotante ado ON ado.id_usuario = ap.id_adotante
WHERE ap.status = 'Ativo'
GROUP BY ado.nome
HAVING SUM(CASE ap.frequencia
               WHEN 'Trimestral' THEN ap.valor_recorrente / 3
               WHEN 'Anual'      THEN ap.valor_recorrente / 12
               ELSE ap.valor_recorrente
           END) > 100
ORDER BY contribuicao_mensal DESC;