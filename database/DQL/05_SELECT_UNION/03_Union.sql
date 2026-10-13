-- Union de Usuario com Inner Join de Adotante/Instituição + Usuario Telefone
SELECT 
    a.nome AS nome_ou_razao,
    'Adotante' AS tipo_perfil,
    u.email,
    ut.telefone
FROM Usuario u
INNER JOIN Adotante a ON u.id_usuario = a.id_usuario
INNER JOIN Usuario_Telefone ut ON u.id_usuario = ut.id_usuario

UNION

SELECT 
    i.razao_social AS nome_ou_razao,
    'Instituição / ONG' AS tipo_perfil,
    u.email,
    ut.telefone
FROM Usuario u
INNER JOIN Instituicao i ON u.id_usuario = i.id_usuario
INNER JOIN Usuario_Telefone ut ON u.id_usuario = ut.id_usuario;

-- Mostra lista unificada de contatos de usuários do tipo adotante e instituição