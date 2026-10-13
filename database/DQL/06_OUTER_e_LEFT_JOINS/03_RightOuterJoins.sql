-- 6.3 RIGHT OUTER JOIN: todos os usuários com seus telefones
SELECT u.id_usuario, u.email, u.tipo_usuario, t.telefone
FROM usuario_telefone t
RIGHT OUTER JOIN usuario u ON u.id_usuario = t.id_usuario;
