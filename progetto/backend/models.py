from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from database import Base


class StatoAnnuncio(enum.Enum):
    APERTO = "aperto"
    ASSEGNATO = "assegnato"
    IN_CONSEGNA = "in_consegna"
    CONSEGNATO = "consegnato"
    ANNULLATO = "annullato"


# Modelli
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relazioni
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    annunci = relationship("Annuncio", back_populates="mittente")
    offerte = relationship("Offerta", back_populates="corriere")
    recensioni_ricevute = relationship("Recensione", back_populates="recensito", foreign_keys="Recensione.recensito_id")
    recensioni_fatte = relationship("Recensione", back_populates="recensore", foreign_keys="Recensione.recensore_id")
    messaggi_inviati = relationship("Messaggio", back_populates="mittente", foreign_keys="Messaggio.mittente_id")
    messaggi_ricevuti = relationship("Messaggio", back_populates="destinatario",
                                     foreign_keys="Messaggio.destinatario_id")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    indirizzo = Column(String)
    citta = Column(String)
    cap = Column(String)
    telefono = Column(String)
    zona_operativa = Column(String, nullable=True)
    raggio_km = Column(Integer, nullable=True)
    veicolo = Column(String, nullable=True)
    patente = Column(String, nullable=True)
    partita_iva = Column(String, nullable=True)
    rating_medio = Column(Float, default=0.0)

    # Relazione inversa con User
    user = relationship("User", back_populates="profile")


class Annuncio(Base):
    __tablename__ = "annunci"

    id = Column(Integer, primary_key=True, index=True)
    mittente_id = Column(Integer, ForeignKey("users.id"))
    titolo = Column(String)
    descrizione = Column(Text)
    indirizzo_ritiro = Column(String)
    indirizzo_consegna = Column(String)
    citta_ritiro = Column(String)
    citta_consegna = Column(String)
    data_ritiro = Column(DateTime)
    stato = Column(String, default=StatoAnnuncio.APERTO.value)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relazioni
    mittente = relationship("User", back_populates="annunci")
    offerte = relationship("Offerta", back_populates="annuncio")


class Offerta(Base):
    __tablename__ = "offerte"

    id = Column(Integer, primary_key=True, index=True)
    annuncio_id = Column(Integer, ForeignKey("annunci.id"))
    corriere_id = Column(Integer, ForeignKey("users.id"))
    prezzo = Column(Float)
    note = Column(Text, nullable=True)
    stato = Column(String, default="in_attesa")  # in_attesa, accettata, rifiutata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relazioni
    annuncio = relationship("Annuncio", back_populates="offerte")
    corriere = relationship("User", back_populates="offerte")


class Recensione(Base):
    __tablename__ = "recensioni"

    id = Column(Integer, primary_key=True, index=True)
    recensore_id = Column(Integer, ForeignKey("users.id"))
    recensito_id = Column(Integer, ForeignKey("users.id"))
    annuncio_id = Column(Integer, ForeignKey("annunci.id"))
    voto = Column(Integer)  # da 1 a 5
    commento = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relazioni
    recensore = relationship("User", foreign_keys=[recensore_id], back_populates="recensioni_fatte")
    recensito = relationship("User", foreign_keys=[recensito_id], back_populates="recensioni_ricevute")
    annuncio = relationship("Annuncio")


class Messaggio(Base):
    __tablename__ = "messaggi"

    id = Column(Integer, primary_key=True, index=True)
    mittente_id = Column(Integer, ForeignKey("users.id"))
    destinatario_id = Column(Integer, ForeignKey("users.id"))
    annuncio_id = Column(Integer, ForeignKey("annunci.id"), nullable=True)
    contenuto = Column(Text)
    letto = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relazioni
    mittente = relationship("User", foreign_keys=[mittente_id], back_populates="messaggi_inviati")
    destinatario = relationship("User", foreign_keys=[destinatario_id], back_populates="messaggi_ricevuti")
    annuncio = relationship("Annuncio")