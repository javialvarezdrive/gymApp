-- database/database_schema.sql

CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nip VARCHAR(6) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    section VARCHAR(255),
    grupo VARCHAR(10),
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    is_monitor BOOLEAN DEFAULT FALSE, -- Indica si el agente es monitor
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE activities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL, -- Ej: "Defensa Personal", "Acondicionamiento Físico"
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE gym_reservations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    activity_id UUID REFERENCES activities(id) NOT NULL,
    monitor_id UUID REFERENCES agents(id) NOT NULL, -- Monitor que imparte la actividad (agente con is_monitor = TRUE)
    reservation_date DATE NOT NULL,
    time_slot VARCHAR(50) NOT NULL, -- "Mañana", "Tarde", "Noche"
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (reservation_date, time_slot, monitor_id) -- Evita reservas duplicadas para el mismo monitor en el mismo turno/día
);

CREATE TABLE agent_activities ( -- Tabla de unión para agentes y actividades (muchos a muchos)
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID REFERENCES agents(id) NOT NULL,
    gym_reservation_id UUID REFERENCES gym_reservations(id) NOT NULL,
    attended BOOLEAN DEFAULT FALSE, -- Para registrar si el agente asistió
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (agent_id, gym_reservation_id) -- Evita duplicados
);


-- Insertar actividades iniciales
INSERT INTO activities (name) VALUES ('Defensa Personal');
INSERT INTO activities (name) VALUES ('Acondicionamiento Físico');

-- Asegúrate de habilitar Row Level Security (RLS) en Supabase y definir políticas de acceso adecuadas para cada tabla.
-- Esto es CRUCIAL para la seguridad.
-- (Configuración de RLS se hace en el panel de Supabase, sección "Authentication" -> "Policies")
