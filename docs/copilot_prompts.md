👤 Kullanıcı Modeli
python

# Create a FastAPI SQLAlchemy model for User with id, username, email, password_hash, and created_at fields.

# username and email must be unique, created_at should auto-set the current UTC time.

🔐 Auth Router
python

# Write a FastAPI router for user registration and login endpoints using Pydantic schema and bcrypt hashing.

# Validate unique email, hash password on register, and verify password on login.

🎨 Palette Model
python

# Define a SQLAlchemy model named Palette with id, user_id (foreign key to User), name, description, is_public, tags and created_at.

# Also define a relationship with User.

🧾 Palette Router
python

# Create a FastAPI router for palettes with CRUD operations (GET, POST, PUT, DELETE).

# Use Pydantic schemas for request/response.

# Include tag handling as a list of strings (case-insensitive search supported).

🌈 Color Model
python

# Define a Color model with id, user_id, hex_code, rgb_r, rgb_g, rgb_b,

# cmyk_c, cmyk_m, cmyk_y, cmyk_k, lab_l, lab_a, lab_b, h, s, l, name, note, created_at.

# Establish relationship with User.

🎨 Color Router
python

# Create a FastAPI router for colors with create, list and delete endpoints.

# Validate unique hex_code per user before insertion.

# Return color id, HEX, and timestamp in the response.

🗃️ Database Helper
python

# Write a dependency function get_db() that yields an SQLAlchemy DB session.

# Ensure it closes automatically at the end of each request.

🔑 JWT Authentication
python

# Implement JWT token generation and verification utilities.

# Use SECRET_KEY, ALGORITHM, and ACCESS_TOKEN_EXPIRE_MINUTES environment variables.

# Add a dependency that validates the Authorization header and injects current user.

🩺 Health Check
python

# Add a GET /health endpoint returning {"status": "ok", "timestamp": "<UTC time>"}.

🔗 Palette–Color Relationship
python

# Create an association table PaletteColor with id, palette_id, color_id, ratio fields.

# Define relationships between Palette and Color models.

⚗️ Mix Result
python

# Define a MixResult model with id, palette_id, result_color_id, target_color_id,

# accuracy (float), and created_at timestamp.

# Link Palette and Color via relationships.

🧮 Renk Karıştırma Fonksiyonu
python

# Implement a Python function mix_colors(colors: list[tuple[int,int,int]], weights: list[float]) -> tuple[int,int,int]

# Calculate weighted average of RGB values.

🧩 API Dokümantasyonu
python

# Add descriptive docstrings, response models, and error codes for FastAPI routes.

# Assign appropriate tags for Swagger UI grouping.

🗂️ Commit ve Git Yardımı
bash

# suggest a commit message in conventional commit format for adding new palette router

# example: feat(api): add palette CRUD endpoints
