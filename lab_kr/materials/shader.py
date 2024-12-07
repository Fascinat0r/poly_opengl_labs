# shader.py
import glm

import OpenGL.GL as gl


class Shader:
    def __init__(self, vertex_source_path: str, fragment_source_path: str):
        # Чтение исходников шейдеров
        with open(vertex_source_path, 'r') as file:
            vertex_source = file.read()
        with open(fragment_source_path, 'r') as file:
            fragment_source = file.read()

        # Создание и компиляция вершинного шейдера
        vertex_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        gl.glShaderSource(vertex_shader, vertex_source)
        gl.glCompileShader(vertex_shader)
        self._check_compile_errors(vertex_shader, "VERTEX")

        # Создание и компиляция фрагментного шейдера
        fragment_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        gl.glShaderSource(fragment_shader, fragment_source)
        gl.glCompileShader(fragment_shader)
        self._check_compile_errors(fragment_shader, "FRAGMENT")

        # Создание шейдерной программы и связывание шейдеров
        self._program = gl.glCreateProgram()
        gl.glAttachShader(self._program, vertex_shader)
        gl.glAttachShader(self._program, fragment_shader)
        gl.glLinkProgram(self._program)
        self._check_compile_errors(self._program, "PROGRAM")

        # Удаление шейдеров после связывания
        gl.glDeleteShader(vertex_shader)
        gl.glDeleteShader(fragment_shader)

    def use(self):
        gl.glUseProgram(self._program)

    def set_bool(self, name: str, value: bool):
        location = gl.glGetUniformLocation(self._program, name)
        gl.glUniform1i(location, int(value))

    def set_int(self, name: str, value: int):
        location = gl.glGetUniformLocation(self._program, name)
        gl.glUniform1i(location, value)

    def set_float(self, name: str, value: float):
        location = gl.glGetUniformLocation(self._program, name)
        gl.glUniform1f(location, value)

    def set_vec2(self, name: str, value):
        location = gl.glGetUniformLocation(self._program, name)
        if isinstance(value, glm.vec2):
            gl.glUniform2fv(location, 1, glm.value_ptr(value))
        else:
            gl.glUniform2f(location, *value)

    def set_vec3(self, name: str, value):
        location = gl.glGetUniformLocation(self._program, name)
        if isinstance(value, glm.vec3):
            gl.glUniform3fv(location, 1, glm.value_ptr(value))
        else:
            gl.glUniform3f(location, *value)

    def set_vec4(self, name: str, value):
        location = gl.glGetUniformLocation(self._program, name)
        if isinstance(value, glm.vec4):
            gl.glUniform4fv(location, 1, glm.value_ptr(value))
        else:
            gl.glUniform4f(location, *value)

    def set_mat2(self, name: str, mat):
        location = gl.glGetUniformLocation(self._program, name)
        gl.glUniformMatrix2fv(location, 1, gl.GL_FALSE, glm.value_ptr(mat))

    def set_mat3(self, name: str, mat):
        location = gl.glGetUniformLocation(self._program, name)
        gl.glUniformMatrix3fv(location, 1, gl.GL_FALSE, glm.value_ptr(mat))

    def set_mat4(self, name: str, mat):
        location = gl.glGetUniformLocation(self._program, name)
        gl.glUniformMatrix4fv(location, 1, gl.GL_FALSE, glm.value_ptr(mat))

    @staticmethod
    def _check_compile_errors(shader, shader_type):
        if shader_type != "PROGRAM":
            success = gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS)
            if not success:
                info_log = gl.glGetShaderInfoLog(shader)
                raise Exception(f"ERROR::SHADER_COMPILATION_ERROR of type: {shader_type}\n{info_log.decode()}")
        else:
            success = gl.glGetProgramiv(shader, gl.GL_LINK_STATUS)
            if not success:
                info_log = gl.glGetProgramInfoLog(shader)
                raise Exception(f"ERROR::PROGRAM_LINKING_ERROR of type: {shader_type}\n{info_log.decode()}")
