-- 使用数据库
USE `nyeweb`;

-- 插入文章数据
INSERT INTO `articles` (`title`, `slug`, `category`, `date`, `summary`, status)
VALUES ('Logistic Regression 笔记', 'Logistic', '机器学习/分类算法', '2023-09-15',
        '本文详细介绍了逻辑回归的原理、数学推导以及在二分类问题中的应用，是机器学习入门的重要概念。', 1),
       ('SVM 学习笔记', 'SVM', '机器学习/分类算法', '2023-09-28',
        '支持向量机（SVM）是一种强大的分类算法。本文探讨了其核心思想，包括最大间隔、核技巧和软间隔等。', 1),
       ('Introduction to Python Programming', 'Introduction to Python Programming', '其他', '2023-10-05',
        '一篇面向初学者的Python入门教程，涵盖了基本语法、数据类型、控制流以及函数等核心编程概念。', 1),
       ('人工智能简介', '人工智能简介', '其他', '2023-10-10',
        '本文简要介绍人工智能的基本概念、发展历史、应用领域以及未来趋势，帮助读者快速了解AI技术。', 1),
       ('Web开发入门', 'Web开发入门', '前端', '2023-10-12',
        '本文介绍Web开发的基础知识，包括HTML、CSS和JavaScript的核心概念、简单示例以及学习资源，适合初学者快速上手。', 1),
       ('个人博客搭建指南', 'personal-blogging-guide', '前端', '2023-10-22',
        '本文详细介绍如何从零开始搭建个人博客，包括平台选择、域名注册、内容创作、SEO优化和流量变现等完整流程，适合初学者快速入门。', 1),
       ('机器学习入门与实践', 'machine-learning-introduction', '其他', '2023-10-25',
        '本文全面介绍机器学习的基本概念、常用算法、实践步骤以及Python代码示例，帮助初学者系统掌握机器学习基础并能够动手实践。', 1),
       ('云计算入门', 'introduction-to-cloud-computing', '其他', '2023-10-18',
        '本文介绍云计算的基本概念、主要服务提供商（如AWS和Azure）、核心服务模型以及入门实践，帮助读者快速理解云技术并开始使用。', 1),
       ('DevOps实践指南', 'devops-practical-guide', '其他', '2023-10-28',
        '本文深入介绍DevOps的核心概念、工具链、实践方法和完整流水线搭建，包含详细的代码示例和最佳实践，帮助团队实现高效的软件交付。', 1),
       ('数据科学基础', 'data-science-basics', '其他', '2023-10-15',
        '本文介绍数据科学的基本概念、常用工具（如Python和pandas）、简单数据分析示例，以及学习资源，帮助初学者快速入门。', 1),
       ('网络安全基础', 'cybersecurity-fundamentals', '其他', '2023-10-20',
        '本文介绍网络安全的基本概念、常见威胁类型、防护措施以及实用工具，帮助读者建立基础安全意识和防护能力。', 1);

-- 插入项目数据
INSERT INTO `projects` (`title`, `slug`, `date`, `summary`, status)
VALUES ('人脸识别系统 MTCNN+FaceNet', 'FaceLogin', '2024-05-20',
        '一个基于PyQt5的实时人脸检测与识别系统，支持摄像头活体验证、用户注册登录等功能。', 1),
       ('温度数据可视化系统', 'Visualization', '2024-04-15',
        '提供完整的温度数据可视化解决方案，支持使用Matplotlib和PyEcharts生成24种专业图表，满足从基础趋势分析到复杂三维建模的全方位需求。', 1);

-- 插入书籍数据
INSERT INTO `books` (`title`, `description`, `filename`, `cover`, status)
VALUES ('C++从入门到项目实践', '一本关于Git版本控制系统的专业书籍，从基础到高级，内容全面。', 'C++从入门到项目实践',
        '/avatar.jpg', 1),
       ('C++项目开发全程实录', '计算机科学的经典之作，帮助程序员从底层理解计算机的工作原理。', 'C++项目开发全程实录',
        '/avatar.jpg', 1),
       ('Node.js+Express+Vue.js项目开发实战', '全面深入地介绍了JavaScript语言的核心概念和最佳实践。',
        'Node.js+Express+Vue.js项目开发实战', '/avatar.jpg', 1);

-- 插入图表数据
INSERT INTO `figures` (`title`, `description`, `url`, status)
VALUES ('Web应用系统架构', '一个典型的Web应用系统架构图，展示了各组件之间的交互。', 'https://s21.ax1x.com/2025/09/16/pVfLCfe.png', 1),
       ('Vue 3 组件生命周期', '清晰地展示了Vue 3中组件从创建到销毁的完整生命周期钩子。', 'https://s21.ax1x.com/2025/09/16/pVfL9YD.png', 1),
       ('微服务通信模式', '总结了微服务架构中常见的几种服务间通信方式。', 'https://s21.ax1x.com/2025/09/16/pVfqzTK.png', 1);

-- 插入工具数据
INSERT INTO `tools` (`title`, `description`, `url`, status)
VALUES ('JSON Formatter', '一个用于格式化、校验和美化JSON数据的在线工具。', 'https://jsonformatter.curiousconcept.com/', 1),
       ('RegExr', '一个用于学习、构建和测试正则表达式的在线工具。', 'https://regexr.com/', 1),
       ('Can I use...', '提供桌面和移动浏览器对前端Web技术支持的最新兼容性表格。', 'https://caniuse.com/', 1),
       ('TinyPNG', '智能的PNG和JPEG压缩工具，用于优化您的图片。', 'https://tinypng.com/', 1),
       ('Color Hunt', '一个免费开放的色彩灵感平台，提供数千个手工挑选的流行调色板。', 'https://colorhunt.co/', 1),
       ('Postman', 'API开发的协作平台。简化API生命周期的每一步，并简化协作。', 'https://www.postman.com/', 1);

-- 插入所有标签 (使用 INSERT IGNORE 避免重复)
INSERT IGNORE INTO `tags` (`name`)
VALUES ('tag1'),
       ('tag2'),
       ('tag3'),
       ('tag4'),
       ('tag5'),
       ('tag6'),
       ('tag7'),
       ('Git'),
       ('版本控制'),
       ('开发工具'),
       ('计算机系统'),
       ('底层原理'),
       ('CS经典'),
       ('JavaScript'),
       ('前端'),
       ('Web开发'),
       ('架构'),
       ('后端'),
       ('系统设计'),
       ('Vue'),
       ('生命周期'),
       ('微服务'),
       ('分布式'),
       ('PyQt5'),
       ('MTCNN'),
       ('FaceNet'),
       ('PyTorch'),
       ('活体检测'),
       ('dlib'),
       ('Matplotlib'),
       ('PyEcharts'),
       ('数据可视化'),
       ('Python'),
       ('JSON'),
       ('格式化'),
       ('Regex'),
       ('测试'),
       ('CSS'),
       ('HTML'),
       ('兼容性'),
       ('图片优化'),
       ('性能'),
       ('设计'),
       ('色彩'),
       ('UI/UX'),
       ('API');

-- 插入文章与标签的关联关系
-- Logistic Regression 笔记
INSERT INTO `article_tags` (article_id, tag_id)
SELECT (SELECT id FROM articles WHERE slug = 'Logistic'), id
FROM tags
WHERE name IN ('tag1', 'tag2', 'tag3');
-- SVM 学习笔记
INSERT INTO `article_tags` (article_id, tag_id)
SELECT (SELECT id FROM articles WHERE slug = 'SVM'), id
FROM tags
WHERE name IN ('tag2', 'tag3', 'tag4');
-- Introduction to Python Programming
INSERT INTO `article_tags` (article_id, tag_id)
SELECT (SELECT id FROM articles WHERE slug = 'Introduction to Python Programming'), id
FROM tags
WHERE name IN ('tag3', 'tag4', 'tag5');
-- 人工智能简介
INSERT INTO `article_tags` (article_id, tag_id)
SELECT (SELECT id FROM articles WHERE slug = '人工智能简介'), id
FROM tags
WHERE name IN ('tag4', 'tag5', 'tag6');
-- Web开发入门
INSERT INTO `article_tags` (article_id, tag_id)
SELECT (SELECT id FROM articles WHERE slug = 'Web开发入门'), id
FROM tags
WHERE name IN ('tag5', 'tag6', 'tag7');
-- 个人博客搭建指南
INSERT INTO `article_tags` (article_id, tag_id)
SELECT (SELECT id FROM articles WHERE slug = 'personal-blogging-guide'), id
FROM tags
WHERE name IN ('tag6', 'tag7', 'tag1');
-- 机器学习入门与实践
INSERT INTO `article_tags` (article_id, tag_id)
SELECT (SELECT id FROM articles WHERE slug = 'machine-learning-introduction'), id
FROM tags
WHERE name IN ('tag7', 'tag1', 'tag2');
-- 云计算入门
INSERT INTO `article_tags` (article_id, tag_id)
SELECT (SELECT id FROM articles WHERE slug = 'introduction-to-cloud-computing'), id
FROM tags
WHERE name IN ('tag1', 'tag2', 'tag3');
-- DevOps实践指南
INSERT INTO `article_tags` (article_id, tag_id)
SELECT (SELECT id FROM articles WHERE slug = 'devops-practical-guide'), id
FROM tags
WHERE name IN ('tag2', 'tag3', 'tag4');
-- 数据科学基础
INSERT INTO `article_tags` (article_id, tag_id)
SELECT (SELECT id FROM articles WHERE slug = 'data-science-basics'), id
FROM tags
WHERE name IN ('tag3', 'tag4', 'tag5');
-- 网络安全基础
INSERT INTO `article_tags` (article_id, tag_id)
SELECT (SELECT id FROM articles WHERE slug = 'cybersecurity-fundamentals'), id
FROM tags
WHERE name IN ('tag4', 'tag5', 'tag6');

-- 插入项目与标签的关联关系
-- 人脸识别系统 MTCNN+FaceNet
INSERT INTO `project_tags` (project_id, tag_id)
SELECT (SELECT id FROM projects WHERE slug = 'FaceLogin'), id
FROM tags
WHERE name IN ('PyQt5', 'MTCNN', 'FaceNet', 'PyTorch', '活体检测', 'dlib');
-- 温度数据可视化系统
INSERT INTO `project_tags` (project_id, tag_id)
SELECT (SELECT id FROM projects WHERE slug = 'Visualization'), id
FROM tags
WHERE name IN ('Matplotlib', 'PyEcharts', '数据可视化', 'Python');

-- 插入书籍与标签的关联关系
-- C++从入门到项目实践
INSERT INTO `book_tags` (book_id, tag_id)
SELECT (SELECT id FROM books WHERE filename = 'C++从入门到项目实践'), id
FROM tags
WHERE name IN ('Git', '版本控制', '开发工具');
-- C++项目开发全程实录
INSERT INTO `book_tags` (book_id, tag_id)
SELECT (SELECT id FROM books WHERE filename = 'C++项目开发全程实录'), id
FROM tags
WHERE name IN ('计算机系统', '底层原理', 'CS经典');
-- Node.js+Express+Vue.js项目开发实战
INSERT INTO `book_tags` (book_id, tag_id)
SELECT (SELECT id FROM books WHERE filename = 'Node.js+Express+Vue.js项目开发实战'), id
FROM tags
WHERE name IN ('JavaScript', '前端', 'Web开发');

-- 插入图表与标签的关联关系
-- Web应用系统架构
INSERT INTO `figure_tags` (figure_id, tag_id)
SELECT (SELECT id FROM figures WHERE url = 'https://s21.ax1x.com/2025/09/16/pVfLCfe.png'), id
FROM tags
WHERE name IN ('tag1', 'tag2', 'tag3');
-- Vue 3 组件生命周期
INSERT INTO `figure_tags` (figure_id, tag_id)
SELECT (SELECT id FROM figures WHERE url = 'https://s21.ax1x.com/2025/09/16/pVfL9YD.png'), id
FROM tags
WHERE name IN ('Vue', '前端', '生命周期');
-- 微服务通信模式
INSERT INTO `figure_tags` (figure_id, tag_id)
SELECT (SELECT id FROM figures WHERE url = 'https://s21.ax1x.com/2025/09/16/pVfqzTK.png'), id
FROM tags
WHERE name IN ('微服务', '架构', '分布式');

-- 插入工具与标签的关联关系
-- JSON Formatter
INSERT INTO `tool_tags` (tool_id, tag_id)
SELECT (SELECT id FROM tools WHERE title = 'JSON Formatter'), id
FROM tags
WHERE name IN ('JSON', '开发工具', '格式化');
-- RegExr
INSERT INTO `tool_tags` (tool_id, tag_id)
SELECT (SELECT id FROM tools WHERE title = 'RegExr'), id
FROM tags
WHERE name IN ('Regex', '开发工具', '测试');
-- Can I use...
INSERT INTO `tool_tags` (tool_id, tag_id)
SELECT (SELECT id FROM tools WHERE title = 'Can I use...'), id
FROM tags
WHERE name IN ('CSS', 'HTML', 'JavaScript', '兼容性');
-- TinyPNG
INSERT INTO `tool_tags` (tool_id, tag_id)
SELECT (SELECT id FROM tools WHERE title = 'TinyPNG'), id
FROM tags
WHERE name IN ('图片优化', '性能', '设计');
-- Color Hunt
INSERT INTO `tool_tags` (tool_id, tag_id)
SELECT (SELECT id FROM tools WHERE title = 'Color Hunt'), id
FROM tags
WHERE name IN ('色彩', '设计', 'UI/UX');
-- Postman
INSERT INTO `tool_tags` (tool_id, tag_id)
SELECT (SELECT id FROM tools WHERE title = 'Postman'), id
FROM tags
WHERE name IN ('API', '开发工具', '测试');

-- 插入时间线数据
INSERT INTO `timeline` (`timestamp`, `content`)
VALUES ('2025-08-25 00:00:00', '网站开始搭建'),
       ('2025-09-01 00:00:00', '完成了初步的页面布局和组件化。'),
       ('2025-09-15 00:00:00', '添加了知识文章模块，并实现了Markdown文件的动态渲染。'),
       ('2025-09-22 00:00:00', '引入了KaTeX来支持数学公式的渲染。'),
       ('2025-10-05 00:00:00', '将数据源切换为JSON文件，为后续连接数据库做准备。'),
       ('2025-10-10 00:00:00', '优化了整体UI，统一了卡片圆角和布局对齐。');

-- 插入收藏图片数据
INSERT INTO `favorite_images` (`url`)
VALUES ('https://s21.ax1x.com/2025/09/16/pVfLCfe.png'),
       ('https://s21.ax1x.com/2025/09/16/pVfL9YD.png'),
       ('https://s21.ax1x.com/2025/09/16/pVfqzTK.png'),
       ('https://s21.ax1x.com/2025/09/16/pVfqxw6.png'),
       ('https://s21.ax1x.com/2025/09/16/pVfqvex.jpg');